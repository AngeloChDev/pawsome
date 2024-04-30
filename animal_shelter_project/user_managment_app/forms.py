from django import forms
from .models import CustomUser, Shelter
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.conf import settings 

dispatch = settings.DISPATCH

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'street_address', 'city', 'country', 'image']


class ShelterSignUpForm(UserCreationForm):
    shelter_name = forms.CharField(max_length=50)
    website = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'street_address', 'city', 'country', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_shelter = True  # Set is_shelter to True
        user.save()
        d=0
        if 'description' in self.cleaned_data.keys() and len(self.cleaned_data['description'])>1:
            d = dispatch('description','save',obj=self.cleaned_data['description'])
        
        shelter = Shelter.objects.create(
            user=user,
            shelter_name=self.cleaned_data['shelter_name'],
            website=self.cleaned_data['website'],
            description=d
        )
        
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser

class ShelterPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Shelter

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'street_address', 'city', 'country', 'image']

        widgets = {
        'profile_image': forms.FileInput(attrs={'class': 'details-section'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance
        self.fields.pop('password')
        self.fields['username'].help_text = ''

class ShelterChangeForm(UserChangeForm):
    class Meta:
        model = Shelter
        fields = ['shelter_name','website', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance
        shelter_instance = user.shelter_set.get()
        self.fields['email'] = forms.EmailField(label='Email', initial= user.email)
        self.fields['username'] = forms.CharField(label='Username', initial= user.username)
        self.fields['street_address'] = forms.CharField(label='Street_address', initial=user.street_address)
        self.fields['city']= forms.CharField(label='City', initial=user.city)
        self.fields['country'] = forms.CharField(label='Country', initial=user.country)
        self.fields['phone_number'] = forms.CharField(label='Phone_number', initial=user.phone_number)
        self.fields['image'] = forms.ImageField(label='Image', initial=user.image)
        if shelter_instance:  # Check if there is a related Shelter instance
            self.fields['shelter_name'].initial = shelter_instance.shelter_name
            self.fields['website'].initial = shelter_instance.website
            self.fields['description'].initial = dispatch('description','get',pk=shelter_instance.description)
        self.fields.pop('password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
    
        if email != user.email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = self.instance

           
        if username != user.username and CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')

        return username

    def save(self, commit=True):
        shelter = super().save(commit=False)
        custom_user_instance = self.instance
        shelter_instance = custom_user_instance.shelter_set.first()  # Access the related Shelter instance
        custom_user_instance.email = self.cleaned_data['email']
        custom_user_instance.username = self.cleaned_data['username']
        custom_user_instance.street_address = self.cleaned_data['street_address']
        custom_user_instance.city = self.cleaned_data['city']
        custom_user_instance.country = self.cleaned_data['country']
        custom_user_instance.phone_number = self.cleaned_data['phone_number']
        custom_user_instance.image = self.cleaned_data['image']
        
        custom_user_instance.save()
        if shelter_instance:  # Check if there is a related Shelter instance
            shelter_instance.shelter_name = self.cleaned_data['shelter_name']
            shelter_instance.website = self.cleaned_data['website']
            if 'description' in self.cleaned_data.keys() and len(self.cleaned_data['description'])>1:
                description = dispatch('description','update',obj=self.cleaned_data['description'],pk=shelter_instance.description)
                shelter_instance.description = description
            
            shelter_instance.save()
            
        if commit:
            shelter.save()
        return shelter
from django.db.models.signals import post_save
from django.dispatch import receiver


#@receiver(post_save, sender=CustomUserForm.Meta.model)
#def handle_model1_post_save(sender, instance, created,**kwargs):
#    if created:
#        print('oooo')
#        code =201 if not instance.is_shelter else 202
#
#        data={'reciver':instance,'code':code}
#        return dispatch('message','send',obj=data )
#        # Esegui azioni quando un'istanza di Model1 viene creata
        
