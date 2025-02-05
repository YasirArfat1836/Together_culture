from django.contrib import admin
from .models import MemberProfile, Event, EventAttendance, DigitalContent, TimeBank

admin.site.register(MemberProfile)
admin.site.register(Event)
admin.site.register(EventAttendance)
admin.site.register(DigitalContent)
admin.site.register(TimeBank)
