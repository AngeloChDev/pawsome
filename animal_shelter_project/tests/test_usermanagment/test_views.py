from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_managment_app.models import CustomUser, Shelter
from user_managment_app.serializers import CustomUserSerializer, ShelterSerializer

class CustomUserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.custom_user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.shelter = Shelter.objects.create(name='Test Shelter', address='123 Test Street')
        
    def test_get_custom_user_list(self):
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.custom_user.username)
    
    def test_get_custom_user_detail(self):
        url = reverse('customuser-detail', args=[self.custom_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.custom_user.username)
    
    def test_get_shelter_list(self):
        url = reverse('shelter-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.shelter.name)
    
    def test_get_shelter_detail(self):
        url = reverse('shelter-detail', args=[self.shelter.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.shelter.name)