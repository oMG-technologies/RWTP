from django.urls import path

from .views import APIGetTranslations

urlpatterns = [
    path('translation/', APIGetTranslations.as_view(), name='api_list')
]
