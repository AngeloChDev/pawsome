from django.test import TestCase
from animal_shelter_app.forms import AddPetForm, ApplicationForm

class AddPetFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'Fluffy',
            'species': 'Cat',
            'gender': 'Female',
            'size': 'Small',
            'message': 'I would love to adopt Fluffy!',
        }
        form = AddPetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'name': '',
            'species': 'Cat',
            'gender': 'Female',
            'size': 'Small',
            'message': 'I would love to adopt Fluffy!',
        }
        form = AddPetForm(data=form_data)
        self.assertFalse(form.is_valid())