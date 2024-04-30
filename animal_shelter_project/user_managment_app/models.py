from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from typing import Any
import requests
from .utils import dispatch

class CustomUser(AbstractUser):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    is_shelter = models.BooleanField(default=False)
    map=models.IntegerField(null=True,editable=False)

    @property
    def data_location(self):
        return {'street_address':self.street_address,'city':self.city,'country':self.country,'name':self.username}


    def set_location(self,**kwargs):
        self.map=dispatch('address','save',self.data_location)
        self.save()
        return self.map
       

    @property
    def get_map(self):
        res=requests.get(f'http://127.0.0.1:8001/api/address/{self.location}/getaddress/')
        return res.data #res.json()['locations']

    @property
    def get_location(self):
        location=dispatch('address','get',pk=self.location)
        return location
        
    @property
    def location(self):
        if self.map is None:
            return self.set_location()
        return self.map
    
    def update(self):
        l=self.location
        self.map=dispatch('address','update',self.data_location,pk=l)
        self.save()

class Shelter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    shelter_name = models.CharField(max_length=50)
    website = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    map=models.IntegerField(null=True,editable=False)

    def __str__(self):
        return self.shelter_name
    
    @property
    def data_location(self):
        return {'street_address':self.user.street_address,'city':self.user.city,'country':self.user.country,'name':self.shelter_name}

    @property
    def get_description(self):
        req= dispatch('description','get',pk=self.description)
        return req

    def set_location(self):
        self.map=dispatch('address','save',self.data_location)
        self.save()
        return self.map
    @property
    def get_location(self):
        location=dispatch('address','get',pk=self.location)
        self.cou
        return location
#
#
    def update(self):
        l=self.location
        self.map=dispatch('address','update',self.data_location,pk=l)
        self.save()

    @property
    def location(self):
        if self.map is None:
            return self.set_location()
        return self.map
    
    
