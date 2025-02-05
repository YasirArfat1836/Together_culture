from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MemberProfile, Event, EventAttendance, DigitalContent, TimeBank
from .serializers import (
    GroupSerializer, UserSerializer, MemberProfileSerializer, 
    EventSerializer, EventAttendanceSerializer,
    DigitalContentSerializer, TimeBankSerializer
)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class ContactForm(serializers.Serializer):
      # simple serializer for emails
    email = serializers.EmailField()
    message = serializers.CharField()


# simple endpoint to take the serializer data
class SendEmail(APIView):
      # permission class set to be unauthenticated
    permission_classes = (permissions.AllowAny,)
    # this is where the drf-yasg gets invoked
    @swagger_auto_schema(request_body=ContactForm)
    def post(self, request):
          # serializer object
        serializer = ContactForm(data=request.data)
        # checking for errors
        if serializer.is_valid():
            json = serializer.data
            return Response(
                data={"status": "OK", "message": json},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        profile = MemberProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        attendance = EventAttendance.objects.create(
            event=event,
            user=request.user
        )
        return Response({'status': 'registered'})

class DigitalContentViewSet(viewsets.ModelViewSet):
    queryset = DigitalContent.objects.all()
    serializer_class = DigitalContentSerializer
    permission_classes = [permissions.IsAuthenticated]

class TimeBankViewSet(viewsets.ModelViewSet):
    queryset = TimeBank.objects.all()
    serializer_class = TimeBankSerializer
    permission_classes = [permissions.IsAuthenticated]

def home(request):
    return render(request, 'together_culture_app/home.html')

@login_required
def events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'together_culture_app/events.html', {'events': events})

@login_required
def digital_content(request):
    content = DigitalContent.objects.all().order_by('-created_date')
    return render(request, 'together_culture_app/digital_content.html', {'content': content})

@login_required
def timebank(request):
    offers = TimeBank.objects.filter(is_active=True).order_by('-created_date')
    return render(request, 'together_culture_app/timebank.html', {'offers': offers})

@login_required
def profile(request):
    # Get or create member profile
    member_profile, created = MemberProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'member_type': 'COMMUNITY',  # Default member type
            'primary_interest': 'SHARING',  # Default interest
            'bio': ''  # Empty bio
        }
    )

    context = {
        'member_profile': member_profile,
        'registered_events': EventAttendance.objects.filter(user=request.user).select_related('event'),
        'timebank_offers': TimeBank.objects.filter(user=request.user).order_by('-created_date')
    }
    
    if created:
        messages.info(request, 'Please complete your profile information.')
        
    return render(request, 'together_culture_app/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        member_profile, created = MemberProfile.objects.get_or_create(user=user)

        # Update user information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update member profile
        member_profile.bio = request.POST.get('bio')
        if request.POST.get('member_type'):  # Only update if provided
            member_profile.member_type = request.POST.get('member_type')
        if request.POST.get('primary_interest'):  # Only update if provided
            member_profile.primary_interest = request.POST.get('primary_interest')
        member_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return redirect('profile')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'together_culture_app/register.html', {'form': form})

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        member_profile = MemberProfile.objects.get(user=request.user)
        
        # Delete old profile picture if it exists
        if member_profile.profile_picture:
            member_profile.profile_picture.delete()
        
        # Save new profile picture
        member_profile.profile_picture = request.FILES['profile_picture']
        member_profile.save()
        
        messages.success(request, 'Profile picture updated successfully!')
    return redirect('profile')