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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render

from lib.ResourceView import ResourceRouter
from app.views import EventView, RegistrationView, CommitteeView, MailView, AdminView, CalendarView


router = ResourceRouter()
router.register(['events'], EventView, 'event')
router.register(['events', 'registrations'], RegistrationView, 'registration')
router.register(['committees'], CommitteeView, 'committee')
router.register(['events', 'mail'], MailView, 'mail')

urlpatterns = [
	url(r'^$', lambda request: redirect('event-list'), name='home'),
	url(r'^faq$', lambda request: render(request, 'faq.html'), name='faq'),
	url(r'^calendar$', CalendarView.as_view('show'), name='calendar'),
	url(r'^admin$', AdminView.as_view('show'), name='admin'),
	url(r'^admin/sync-ldap$', AdminView.as_view('sync-ldap'), name='admin-sync-ldap'),
	url(r'^admin/calendar$', AdminView.as_view('calendar'), name='admin-calendar'),
	url(r'^admin/calendar/flow$', AdminView.as_view('calendar-flow'), name='admin-calendar-flow'),
	url(r'^django-admin/', admin.site.urls, name='django-admin'),

	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
]

urlpatterns.extend(router.urls())
