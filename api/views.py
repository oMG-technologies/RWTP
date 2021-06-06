from django.views.generic import TemplateView
from django.http import JsonResponse

from .models import Translation, Language
from .serializers import (TranslationSerializers,
                          LanguageSerializers,
                          SingleTranslationSerializers,
                          UserSerializer,
                          GroupSerializer,)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions


class APIGetTranslations(TemplateView):

    model = Translation

    def get(self, request):
        translation = Translation.objects.all()
        raw_serializer = TranslationSerializers(translation, many=True)
        serializer_data = {}
        serializer_data['questions'] = raw_serializer.data
        return JsonResponse(serializer_data,
                            safe=False,
                            json_dumps_params={'indent': 4})


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers


class SingleTranslationViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SingleTranslationSerializers

    def get_queryset(self):
        '''
        Optionally show translations only for a given conversion,
        by filtering against a `conversion` query parameter in the URL.

        e.g.

        http://127.0.0.1:8000/translation/?conversion=en-de

        will show translation only for en-de conversion

        '''
        queryset = Translation.objects.all()
        conversion = self.request.query_params.get('conversion')
        if conversion is not None:
            queryset = queryset.filter(translation_id=conversion)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
