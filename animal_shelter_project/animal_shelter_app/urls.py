from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'animal_shelter_app'

urlpatterns =[
    path('', PetListView.as_view(), name='pet_list'),
    path('pets/', PetListView.as_view(), name='pet_list'),
    path('pet/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/<int:pk>/', PetListView.as_view(), name='pet_list_shelter'),
    path('add_pet/', AddPetView.as_view(), name='add_pet'), # added by mohsen
    path('adoption-form/<int:pet_id>/', AdoptionCreateView.as_view(), name='adoption_form'), # added by mohsen
    path('adoption-success/', AdoptionSuccessView.as_view(), name='adoption_success'),
    path('pet/<int:pk>/update/', PetUpdateView.as_view(), name='edit_pet_profile'),
    path('manager_adoption/', AdoptionListView.as_view(), name='manager_adopt_applications'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # added by mohsen

