from .models import Translation, Language
from .serializers import (TranslationSerializers,
                          LanguageSerializers,
                          SingleTranslationSerializers,
                          AvailableLanguagesSerializers,
                          UserSerializer,
                          GroupSerializer)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response


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


class AvailableLanguagesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = AvailableLanguagesSerializers

    # def retrieve(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})

    def list(self, request, *args, **kwargs):
        languages = Language.objects.all()
        serializers = self.get_serializer(languages, many=True)
        conversions_list = []
        for id, item in enumerate(serializers.data):
            conversion = {}
            conversion['id'] = id
            conversion['conversion'] = item['conversion']
            conversions_list.append(conversion)

        return Response({'available_conversions': conversions_list})


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


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers


class SingleTranslationViewSet(generics.ListAPIView):
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
