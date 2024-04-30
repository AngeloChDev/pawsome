from django.test import TestCase
from django.contrib.auth import get_user_model
from user_managment_app.models import CustomUser, Shelter

User = get_user_model()

class UserManagementAppModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            street_address='123 Test Street',
            city='Test City',
            country='Test Country',
            phone_number='1234567890'
        )
        self.shelter = Shelter.objects.create(
            user=self.user,
            shelter_name='Test Shelter',
            website='https://testshelter.com',
            description='Test description'
        )

    def test_custom_user_creation(self):
        self.assertEqual(self.user.street_address, '123 Test Street')
        self.assertEqual(self.user.city, 'Test City')
        self.assertEqual(self.user.country, 'Test Country')
        self.assertEqual(self.user.phone_number, '1234567890')

    def test_shelter_creation(self):
        self.assertEqual(self.shelter.user, self.user)
        self.assertEqual(self.shelter.shelter_name, 'Test Shelter')
        self.assertEqual(self.shelter.website, 'https://testshelter.com')
        self.assertEqual(self.shelter.description, 'Test description')

    def test_shelter_string_representation(self):
        self.assertEqual(str(self.shelter), 'Test Shelter')