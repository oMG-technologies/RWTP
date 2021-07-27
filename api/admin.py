from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import Translation, Language

# Register your models here.
admin.site.register(Translation)
admin.site.register(Language)

TokenAdmin.raw_id_fields = ['user']
