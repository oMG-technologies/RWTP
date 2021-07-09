from django.urls import path, include
from rest_framework import routers

from .views import (TranslationsViewSet,
                    LanguageViewSet,
                    AvailableLanguagesViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    GroupViewSet,
                    Audio)

router = routers.DefaultRouter()
router.register(r'translations', TranslationsViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'available_conversions', AvailableLanguagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single_lang'),
    path('media/', Audio.as_view()),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
]
