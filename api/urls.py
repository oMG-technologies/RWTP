from django.urls import path, include
from rest_framework import routers

<<<<<<< HEAD
from .views import (TranslationsViewSet,
                    LanguageViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    GroupViewSet,
                    AvailableLanguagesViewSet)

router = routers.DefaultRouter()
router.register(r'translations', TranslationsViewSet)
router.register(r'language', LanguageViewSet)
=======
from .views import TranslationsViewSet, UserViewSet, GroupViewSet, APIGetTranslations

# ViewSets define the view behavior.


router = routers.DefaultRouter()
router.register(r'translations', TranslationsViewSet)
>>>>>>> 53c1caa (feat: modify api view root to allow to view and edit translations)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'available_conversions', AvailableLanguagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single_lang'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
]
