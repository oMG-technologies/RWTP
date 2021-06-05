from django.urls import path, include
from rest_framework import routers

from .views import (TranslationsViewSet, UserViewSet, GroupViewSet,
                    APIGetTranslations, LanguageViewSet,
                    SingleTranslationViewSet, SingleTranslation)

# ViewSets define the view behavior.


router = routers.DefaultRouter()
router.register(r'translations', TranslationsViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'single', SingleTranslationViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('translations/', APIGetTranslations.as_view(), name='api_list'),
    path('translations/<str:language>',
         SingleTranslation.as_view(), name='single_translation'),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework_test'))
]

urlpatterns += router.urls
