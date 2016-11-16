from django.contrib import admin
from .models import Committee, Event, Registration

admin.site.register([Committee, Event, Registration])
