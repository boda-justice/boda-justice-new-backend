from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models
from rest_framework.exceptions import ValidationError

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}
            

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lawyer
        fields = ['user', 'practise_number', 'building_address', 'street_road', 'building_floor', 'id_number', 'phone_number']


class ComplainantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complainants
        fields = ['user', 'occupation', 'id_number', 'phone_number']


class OffenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offence
        fields = ['description', 'offense_type', 'fine']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Case
        fields = ['lawyer', 'offence', 'status', 'complaint']

class ComplaintSerializer(serializers.ModelSerializer):
    complainant = serializers.ReadOnlyField(source='complainant.username')
    class Meta:
        model = models.Complaint
        fields = ['description', 'location', 'complainant']