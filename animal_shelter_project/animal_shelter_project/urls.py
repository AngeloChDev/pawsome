"""
URL configuration for animal_shelter_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animal_shelter_app.urls')),
    path('', include('user_managment_app.urls')),
    #path('', include('openai_app.urls')),
    path('', include('dashboard.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('home', HomePageView.as_view(), name='home'),#added by mohsen

    
]
