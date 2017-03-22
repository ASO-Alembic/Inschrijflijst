from django.contrib import admin
from .models import Committee, Event, Registration, User

admin.site.register([Committee, Event, Registration, User])
