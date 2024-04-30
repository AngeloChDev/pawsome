from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "user_managment_app"

urlpatterns =[
    #path('profilemap/', map.as_view(), name='profilmap'),
    path('shelters/', ShelterListCreatView.as_view(), name='shelter_list'),
    path('shelter/<int:pk>/', ShelterDetailView.as_view(), name='shelter_detail'),
    path('user/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_user/', SignUpCustomUserView.as_view(), name='signup_customuser'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup_shelter/', SignUpShelterView.as_view(), name='signup_shelter'),
    path('edit_user_profile/', EditCustomUserProfileView.as_view(), name='edit_customuser_profile'),
    path('user_profile/', CustomUserProfileView.as_view(), name='customuser_profile'),
    path('edit_shelter_profile/', EditShelterProfileView.as_view(), name='edit_shelter_profile'),
    path('shelter_profile/', ShelterProfileView.as_view(), name='shelter_profile'),
    path('fullmap/', Fullmap.as_view(), name='fullmap'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # added by mohsen

