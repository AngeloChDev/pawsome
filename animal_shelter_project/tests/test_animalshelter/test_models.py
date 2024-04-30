from django.test import TestCase
from django.contrib.auth import get_user_model
from animal_shelter_app.models import Pet, Application, Shelter

class AnimalShelterAppTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.shelter = Shelter.objects.create(name='Test Shelter')
        self.pet = Pet.objects.create(
            name='Test Pet',
            species='dog',
            breeds='breed',
            age='2',
            gender='male',
            size='medium',
            weight='20',
            photos='test.jpg',
            description='Test description',
            status='adoptable',
            shelter=self.shelter
        )
        self.application = Application.objects.create(
            pet=self.pet,
            user=self.user,
            message='Test application'
        )

    def test_pet_model(self):
        pet = Pet.objects.get(name='Test Pet')
        self.assertEqual(pet.species, 'dog')
        self.assertEqual(pet.status, 'adoptable')

    def test_application_model(self):
        application = Application.objects.get(user=self.user)
        self.assertEqual(application.pet, self.pet)
        self.assertEqual(application.message, 'Test application')

    def test_application_save(self):
        self.assertEqual(self.pet.status, 'adoptable')
        self.application.save()
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, 'pending_adoption')