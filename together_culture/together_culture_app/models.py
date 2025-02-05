import sys
print("Models module path:", __file__, file=sys.stderr)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class MemberProfile(models.Model):
    MEMBER_TYPES = [
        ('COMMUNITY', 'Community Member'),
        ('KEY_ACCESS', 'Key Access Member'),
        ('CREATIVE', 'Creative Workspace Member'),
    ]

    INTEREST_CHOICES = [
        ('CARING', 'Caring'),
        ('SHARING', 'Sharing'),
        ('CREATING', 'Creating'),
        ('EXPERIENCING', 'Experiencing'),
        ('WORKING', 'Working'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPES)
    primary_interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    is_approved = models.BooleanField(default=False)
    join_date = models.DateTimeField(default=timezone.now)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    capacity = models.IntegerField()
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class DigitalContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_url = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TimeBank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_offered = models.CharField(max_length=200)
    skill_needed = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill_offered}"
