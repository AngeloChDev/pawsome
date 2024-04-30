from rest_framework import serializers
from .models import Pet, Application

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breeds', 'age', 'gender', 'size', 'weight', 'photos', 'description', 'status', 'published_at', 'updated_at', 'shelter']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'pet', 'user', 'message']