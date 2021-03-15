from django.contrib import admin
from .models import Committee, Event, Registration, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_seen_at', 'is_superuser', 'is_staff')
    search_fields = ['username']

admin.site.register([Committee, Event, Registration])
