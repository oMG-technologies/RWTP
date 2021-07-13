from django.db.models import query
from django.db.models.query_utils import Q
from .models import Translation, Language
from .serializers import (TranslationSerializers,
                          TranslationDetailSerializers,
                          LanguageSerializers,
                          SingleTranslationSerializers,
                          AvailableLanguagesSerializers,
                          UserSerializer,
                          GroupSerializer)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


# @action(detail=True, methods=['get'])
class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return TranslationDetailSerializers
    #     return TranslationSerializers

    def retrieve(self, request, pk=None):
        queryset = Translation.objects.all()
        trans = get_object_or_404(queryset, pk=pk)
        serializer = TranslationSerializers(trans)
        print('here')
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def single(self, request, pk=None):
        queryset = Translation.objects.get(pk=pk)
        serializer = TranslationSerializers(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        Translation.objects.filter(pk=pk).delete()
        # serializer = TranslationSerializers(queryset)
        return Response({'pk': 'Successfully removed'})


# @action(detail=True, methods=['delete'])
# class TranslationDetail(generics.ListAPIView):
#     serializer_class = TranslationSerializers

#     def get_queryset(self):
#         queryset = Translation.objects.all()
#         id = self.request.query_params.get('id')
#         if id is not None:
#             queryset = queryset.filter(i=id)
#         return queryset


# @action(detail=True, methods=['get'])
class LanguageViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see Languages.
    '''
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers


class LanguageDetail(generics.ListAPIView):
    def get_queryset(self):

        queryset = Language.objects.all()
        pass

    # @action(methods=['get'], detail=True)
    # def delete(self, request):
    #     pass


class AvailableLanguagesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = AvailableLanguagesSerializers

    # ISO 639-1 code has always lenght of 2

    length = 2

    # def retrieve(self, request, *args, **kwargs):
    #     return Response({'something': 'my custom JSON'})

    def list(
            self,
            request,
            *args,
            **kwargs):
        ''' Overwrite the defaut list method to return flatten
        list of conversions '''
        from iso639 import languages
        from .iso639_to_iso3166 import iso_exceptions_dict

        languages_objects = Language.objects.all()
        serializers = self.get_serializer(languages_objects, many=True)
        conversions_list = []
        for id, item in enumerate(serializers.data):
            conversion = {}
            iso639_lang_code = item['conversion'][self.length+1:]
            language_name = languages.get(part1=str(iso639_lang_code)).name

            iso3166_lang_code = iso639_lang_code
            if iso639_lang_code in iso_exceptions_dict:
                iso3166_lang_code = iso_exceptions_dict[iso639_lang_code]

            # prepare a json response
            conversion['id'] = id
            conversion['conversion'] = item['conversion']
            conversion['target_language_iso639'] = iso639_lang_code
            conversion['target_language_iso3166'] = iso3166_lang_code
            conversion['name'] = language_name
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
