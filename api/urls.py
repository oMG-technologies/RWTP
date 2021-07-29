from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (UserProgress,
                    TranslationsViewSet,
                    LanguageViewSet,
                    AvailableLanguagesViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    isUser,
                    UserCreateViewSet,
                    UserDeleteViewSet,
                    GroupViewSet,
                    )

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'translations',
                TranslationsViewSet, basename='translations')
router.register(r'language', LanguageViewSet, basename='language')
router.register(r'users', UserViewSet, basename='users')
# router.register(r'is_user', isUser, basename='is_User')
router.register(r'user_create', UserCreateViewSet, basename='user_create')
router.register(r'user_delete', UserDeleteViewSet, basename='user_delete')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'available_conversions',
                AvailableLanguagesViewSet, basename='available_conversions')

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single_lang'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
    path('api-token-auth/', views.obtain_auth_token),
    path('user_progress/', UserProgress.as_view(), name='user_progress'),
    path('is_user/<str:username>/', isUser.as_view(), name='is_user')
]
