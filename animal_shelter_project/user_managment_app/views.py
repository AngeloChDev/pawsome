from rest_framework import generics
from rest_framework.response import Response
from .models import CustomUser, Shelter
from .serializers import CustomUserSerializer
from django.shortcuts import render,redirect
from animal_shelter_app.models import Pet
from django.views.generic import CreateView, View, ListView, TemplateView, DetailView
from .forms import CustomUserForm, ShelterSignUpForm, CustomUserChangeForm, ShelterChangeForm 
from django.urls import reverse_lazy
from .forms import ShelterSignUpForm
from django.db import IntegrityError
from animal_shelter_app.models import Application
from filters.forms import PetFilterForm
import json, folium, os
from django.conf import settings 
from rest_framework.permissions import AllowAny
from pathlib import Path
from django.contrib import messages
# messages.success(request,"New Team created","allgood")

 #                 messages.error(request,"Error team name exist","error")
dispatch = settings.DISPATCH



    
class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        shelter_users = CustomUser.objects.filter(is_shelter=True)
        normal_users = CustomUser.objects.filter(is_shelter=False)
        
        shelter_serializer = CustomUserSerializer(shelter_users, many=True)
        normal_serializer = CustomUserSerializer(normal_users, many=True)

        return Response({
            'serializer': serializer.data,
            'shelter': shelter_serializer.data,
            'user': normal_serializer.data
        })

class ShelterListCreatView(generics.ListCreateAPIView):
    queryset = Shelter.objects.all()

    def get(self, request, *args, **kwargs):
        shelters = self.get_queryset()
        users = CustomUser.objects.filter(is_shelter=True)  
        return render(request, 'shelter_list.html', {'shelters': shelters, 'users': users})


class ShelterDetailView(DetailView):
    model = Shelter
    template_name = "shelter_detail.html"
    context_object_name = "shelter"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shelter = self.get_object()
        pets = Pet.objects.filter(shelter=shelter, status__in=['adoptable', 'pending_adoption'])
        form = PetFilterForm(self.request.GET)
        if form.is_valid():
            species = form.cleaned_data.get('species')
            gender = form.cleaned_data.get('gender')
            size = form.cleaned_data.get('size')

            if species:
                pets = pets.filter(species=species)
            if gender:
                pets = pets.filter(gender=gender)
            if size:
                pets = pets.filter(size=size)

        context['pets'] = pets
        context['filter_form'] = form  # Pass the form to the template
        context['map'] = None
        context['locations_user'] = None
        context['locations'] = None
        if self.request.user.is_authenticated:
            context['locations_user'] = self.request.user.get_location
            context['locations'] = shelter.get_location
            try:
                coordinate = f"{context['locations_user']['latitude']} , {context['locations_user']['longitude']} end  {context['locations']['latitude']} , {context['locations']['longitude']}"
                context['map'] = json.dumps(dispatch('address', 'getstreet', coordinate))
            
            except:
                pass
        print(context.keys())
        return context

    
class SignUpView(TemplateView):
    template_name = "registration/signup.html"


class SignUpCustomUserView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup_customuser.html"

class SignUpShelterView(CreateView):
    form_class = ShelterSignUpForm
    template_name = 'registration/signup_shelter.html'
    success_url = reverse_lazy('login')

    

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('username', 'This username is already taken.')
            return self.form_invalid(form)
          
class EditCustomUserProfileView(View):
    template_name = 'edit_customuser_profile.html'

    def get(self, request):
        user = request.user
        form = CustomUserChangeForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_managment_app:customuser_profile')  
        else:
            context = {'form': form}
            return render(request, self.template_name, context)

class EditShelterProfileView(View):
    template_name = 'edit_shelter_profile.html'
    
    def get(self, request):
        user = request.user
        form = ShelterChangeForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        form = ShelterChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect ('user_managment_app:shelter_profile')  
        else:
            context = {'form': form}
            return render(request, self.template_name, context)
        
class CustomUserProfileView(ListView):
    model = CustomUser
    template_name = "customuser_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = Application.objects.filter(user=self.request.user)
        profile = self.get_queryset().first()
        context['profile'] = profile
        context['applications'] = applications
        return context
    

class ShelterProfileView(ListView):
    model = Shelter
    template_name = "shelter_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        return Shelter.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object_list'].first() 
        context['profile'] = profile
        context['locations']=None
        context['locations_user']=None
        context['map']=None
        print(profile.get_location)

        try:
            context['locations'] = profile.get_location 
            
            context['locations']['name']=profile.shelter_name
        except:
            pass
        print('PPP',context['locations'])
        return context
    



class Fullmap(TemplateView):
    template_name='fullmap.html'

    def get_context_data(self) :
        points =dispatch('address','fullmap')
        context={
            'points':points
        }

        m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
        for i in points:
            coord=[i['latitude'], i['longitude']]
            if coord[0]==None or coord[1]==None:
                coord=[50.2345, 10.1234]
            folium.Marker(
                location=coord,
                popup=i['name'],
            ).add_to(m)
        path=Path(settings.BASE_DIR) / 'templates' / 'runtimemap.html'
        m.save(path)
        return context
    
    def get(self,request):
        return render(request, self.template_name,self.get_context_data())
    
