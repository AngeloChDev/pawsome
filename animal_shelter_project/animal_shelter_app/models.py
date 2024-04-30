from django.db import models
from django.contrib.auth.models import AbstractUser
from user_managment_app.models import CustomUser, Shelter
from user_managment_app.utils import dispatch


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat')
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ]

    STATUS_CHOICES = [
        ('adoptable', 'Adoptable'),
        ('pending_adoption', 'Pendingadoption'),
        ( 'adopted', 'Adopted')
    ]

    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breeds = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    weight = models.CharField(max_length=50)
    photos = models.ImageField(upload_to='pets_images')
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species})"
    
    @property
    def get_description(self):
        req= dispatch('description','get',pk=self.description)
        return req
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('Under_review', 'Under review'),
        ('adopted', 'Adopted'),
        ('cancelled', 'Cancelled')
    ]
        
    created_at = models.DateTimeField(auto_now_add=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} ({self.pet})"

    def approve(self):
        self.status = 'adopted'
        self.pet.status = 'adopted'
        self.save()
        self.pet.save()

    def cancel(self):
        self.status = 'cancelled'
        self.save()




