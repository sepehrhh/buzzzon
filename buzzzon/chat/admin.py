from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

admin.site.register(Room)
admin.site.register(Contact)
