from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import MemberProfile, Event, EventAttendance, DigitalContent, TimeBank


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MemberProfile
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendance
        fields = '__all__'


class DigitalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalContent
        fields = '__all__'


class TimeBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeBank
        fields = '__all__'