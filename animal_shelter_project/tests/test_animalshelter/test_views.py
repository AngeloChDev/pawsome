from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from animal_shelter_app.models import Pet, Application
from animal_shelter_app.views import PetListView, PetDetailView, AddPetView, AdoptionCreateView, AdoptionSuccessView, PetUpdateView

class AnimalShelterAppViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.pet = Pet.objects.create(name='Test Pet', species='dog', breeds='breed', age='2', gender='male', size='medium', weight='20', photos='test.jpg', description='Test description', status='adoptable')
        self.application = Application.objects.create(pet=self.pet, user=self.user, message='Test application')

    def test_pet_list_view(self):
        url = reverse('animal_shelter_app:pet_list')
        request = self.factory.get(url)
        response = PetListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pet_list.html')

    def test_pet_detail_view(self):
        url = reverse('animal_shelter_app:pet_detail', kwargs={'pk': self.pet.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = PetDetailView.as_view()(request, pk=self.pet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pet_detail.html')

    def test_add_pet_view(self):
        url = reverse('animal_shelter_app:add_pet')
        request = self.factory.get(url)
        request.user = self.user
        response = AddPetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_pet.html')

    def test_adoption_create_view(self):
        url = reverse('animal_shelter_app:adoption_create', kwargs={'pet_id': self.pet.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = AdoptionCreateView.as_view()(request, pet_id=self.pet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adoption_form.html')

    def test_adoption_success_view(self):
        url = reverse('animal_shelter_app:adoption_success')
        request = self.factory.get(url)
        response = AdoptionSuccessView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adoption_success.html')

    def test_pet_update_view(self):
        url = reverse('animal_shelter_app:pet_update', kwargs={'pk': self.pet.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = PetUpdateView.as_view()(request, pk=self.pet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_pet_profile.html')