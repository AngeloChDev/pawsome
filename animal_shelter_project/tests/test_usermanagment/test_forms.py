from django.test import TestCase
from django.contrib.auth import get_user_model
from user_managment_app.forms import CustomUserForm, ShelterSignUpForm, CustomPasswordChangeForm, ShelterPasswordChangeForm, CustomUserChangeForm, ShelterChangeForm

from user_managment_app.models import CustomUser, Shelter
User = get_user_model()

class UserManagementAppFormsTestCase(TestCase):
    def test_custom_user_form_valid_data(self):
        form = CustomUserForm(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'phone_number': '1234567890',
            'street_address': '123 Test Street',
            'city': 'Test City',
            'country': 'Test Country',
            'image': 'test.jpg'
        })
        self.assertTrue(form.is_valid())

    def test_shelter_sign_up_form_valid_data(self):
        form = ShelterSignUpForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'phone_number': '1234567890',
            'street_address': '123 Test Street',
            'city': 'Test City',
            'country': 'Test Country',
            'image': 'test.jpg',
            'shelter_name': 'Test Shelter',
            'website': 'https://testshelter.com',
            'description': 'Test description'
        })
        self.assertTrue(form.is_valid())

    def test_custom_password_change_form_valid_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form = CustomPasswordChangeForm(user=user, data={
            'old_password': 'testpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.assertTrue(form.is_valid())
        
    
    """ def test_shelter_password_change_form_valid_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        shelter = Shelter.objects.create(user=user)
        form = ShelterPasswordChangeForm(user=shelter, data={
        'old_password': 'testpassword',
        'new_password1': 'newpassword',
        'new_password2': 'newpassword'
        })
        
        self.assertTrue(form.is_valid()) """

    def test_shelter_password_change_form_valid_data(self):
        shelter = Shelter.objects.create(user=User)
        form = ShelterPasswordChangeForm(user=shelter, data={
            'old_password': 'testpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.assertTrue(form.is_valid())

    def test_custom_user_change_form_valid_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form = CustomUserChangeForm(instance=user, data={
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'street_address': '123 Test Street',
            'city': 'Test City',
            'country': 'Test Country',
            'image': 'test.jpg'
        })
        self.assertTrue(form.is_valid())

    def test_shelter_change_form_valid_data(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        shelter = Shelter.objects.create(user=user, shelter_name='Test Shelter')
        form = ShelterChangeForm(instance=user, data={
            'shelter_name': 'New Shelter Name',
            'website': 'https://newshelter.com',
            'description': 'New description'
        })
        self.assertTrue(form.is_valid())