"""Inschrijflijst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render

from lib.ResourceView import ResourceRouter
from app.views import EventView, RegistrationView, CommitteeView, MailView, AdminView, CalendarView, StatsView


router = ResourceRouter()
router.register(['events'], EventView, 'event')
router.register(['events', 'registrations'], RegistrationView, 'registration')
router.register(['committees'], CommitteeView, 'committee')
router.register(['events', 'mail'], MailView, 'mail')

urlpatterns = [
	path('', lambda request: redirect('event-list'), name='home'),
	path('faq', lambda request: render(request, 'faq.html'), name='faq'),
	path('calendar', CalendarView.as_view('show'), name='calendar'),
	path('admin', AdminView.as_view('show'), name='admin'),
	path('admin/sync-ldap', AdminView.as_view('sync-ldap'), name='admin-sync-ldap'),
	path('admin/calendar', AdminView.as_view('calendar'), name='admin-calendar'),
	path('admin/calendar/flow', AdminView.as_view('calendar-flow'), name='admin-calendar-flow'),

	re_path(r'^api/stats/events/(\d+)/registrations/$', StatsView.as_view('registrations'), name='api-stats-registrations'),

	path('django-admin/', admin.site.urls, name='django-admin'),
	path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns.extend(router.urls())
