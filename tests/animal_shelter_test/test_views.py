from django.test import TestCase, RequestFactory
from django.urls import reverse
from .animal_shelter_app.models import Pet, Application  # Import from animal_shelter_app.models

class PetViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pet = Pet.objects.create(
            species='Dog',
            gender='Male',
            size='Medium',
            status='Available'
        )
    
    def test_pet_list_view(self):
        url = reverse('pet-list-create')
        request = self.factory.get(url)
        response = PetListCreatView.as_view()(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pet.species)
    
    def test_pet_detail_view(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        request = self.factory.get(url)
        response = PetDetailView.as_view()(request, pk=self.pet.pk)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pet.species)