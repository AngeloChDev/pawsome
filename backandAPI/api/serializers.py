from rest_framework import serializers
from django.core.validators import validate_email
from .models import Media, Description, Address, MessageArchivie


class AddressSerializer(serializers.ModelSerializer):
      class Meta:
            model = Address
            fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
      class Meta:
            model = Media
            fields = '__all__'


class DescriptionSerializer(serializers.ModelSerializer):
      class Meta:
            model = Description
            fields = '__all__'

class MessageArchivieSerializer(serializers.ModelSerializer):
      class Meta:
            model = MessageArchivie
            fields = '__all__'