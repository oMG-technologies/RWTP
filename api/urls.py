from django.urls import path, include
from rest_framework import routers

from .views import (TranslationsViewSet,
                    # TranslationDetail,
                    LanguageViewSet,
                    AvailableLanguagesViewSet,
                    SingleTranslationViewSet,
                    UserViewSet,
                    GroupViewSet
                    )

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'translations',
                TranslationsViewSet, basename='translations')
# router.register(r'tran', TranslationDetailViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'available_conversions', AvailableLanguagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('translation/', SingleTranslationViewSet.as_view(),
         name='translation_single_lang'),
    #     path(
    #         'trans/', TranslationDetail.as_view(), name='trans_pk'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test')),
]
