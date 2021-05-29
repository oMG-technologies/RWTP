from django.urls import path

from .views import APIGetTranslations

urlpatterns = [
    path('translations/', APIGetTranslations.as_view(), name='api_list')
]
