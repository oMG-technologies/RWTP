from django.urls import path, include
from rest_framework import routers

from .views import (TranslationsViewSet,
                    LanguageViewSet,
                    AvailableLanguagesViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    UserCreateViewSet,
                    UserDeleteViewSet,
                    GroupViewSet
                    )

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'translations',
                TranslationsViewSet, basename='translations')
router.register(r'language', LanguageViewSet, basename='language')
router.register(r'users', UserViewSet, basename='users')
router.register(r'user_create', UserCreateViewSet, basename='user_create')
router.register(r'user_delete', UserDeleteViewSet, basename='user_delete')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'available_conversions', AvailableLanguagesViewSet, basename='available_conversions')

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single_lang'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
]
