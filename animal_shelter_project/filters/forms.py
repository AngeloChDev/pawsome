from django import forms
from animal_shelter_app.models import Pet

class PetFilterForm(forms.Form):
    SPECIES_CHOICES = [
        ('', 'All Species'),
        ('dog', 'Dog'),
        ('cat', 'Cat')
    ]

    GENDER_CHOICES = [
        ('', 'All Genders'),
        ('male', 'Male'),
        ('female', 'Female')
    ]

    SIZE_CHOICES = [
        ('', 'All Sizes'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ]

    species = forms.ChoiceField(choices=SPECIES_CHOICES, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)
