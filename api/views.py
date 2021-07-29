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
from rest_framework.decorators import action
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint view that allows to see translations.
    '''
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers

    @action(detail=True, methods=['get'])
    def single(self, request, pk=None):
        queryset = Translation.objects.get(pk=pk)
        serializer = TranslationSerializers(queryset)
        return Response(serializer.data)

    @csrf_exempt
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        Translation.objects.filter(pk=pk).delete()
        return Response({'pk': 'Successfully removed'})

    @csrf_exempt
    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):

        data = request.data

        conversion = data['conversion']
        i = data['i']
        frontCard = data['frontCard']
        backCard = data['backCard']
        pronunciation_frontCard = data['pronunciation_frontCard']
        pronunciation_backCard = data['pronunciation_backCard']
        source_language = data['source_language']
        target_language = data['target_language']

        try:
            Language.objects.create(
                conversion=conversion,
            )
        except IntegrityError:
            pass

        language_obj = Language.objects.filter(
            conversion__contains=conversion)[0]
        Translation.objects.create(
            translation=language_obj,
            i=i,
            frontCard=frontCard,
            backCard=backCard,
            pronunciation_frontCard=pronunciation_frontCard,
            pronunciation_backCard=pronunciation_backCard,
            source_language=source_language,
            target_language=target_language,
        )
        return Response({'POST': 'Object created successfully!'})


class LanguageViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see Languages.
    '''
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers
    lookup_field = 'conversion'

    @action(detail=True, methods=['get'])
    def single(self, request, conversion=None):
        queryset = Language.objects.get(conversion=conversion)
        serializer = LanguageSerializers(queryset)
        return Response(serializer.data)

    @csrf_exempt
    @action(detail=True, methods=['delete'])
    def delete(self, request, conversion=None):
        Language.objects.filter(conversion=conversion).delete()
        return Response({'Conversion': 'Successfully removed'})


class AvailableLanguagesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Language.objects.all()
    serializer_class = AvailableLanguagesSerializers

    # ISO 639-1 code has always lenght of 2
    length = 2

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


class TranslationsViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to see translations.
    '''
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializers
    # permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return User.objects.all()
    #     return User.objects.filter(username=user.username)


class UserCreateViewSet(UserViewSet):
    permission_classes = [permissions.AllowAny]
    # lookup_field = 'username'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @action(detail=True, methods=['PUT'])
    def add(self, request, pk=None):
        data = request.data
        serialized = UserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']

        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password)

        current_user = User.objects.get(username=username)
        current_user.set_password(password)
        current_user.save()

        return Response({'User created successfully': serialized.data})


class UserDeleteViewSet(UserViewSet):
    lookup_field = 'username'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @action(detail=True, methods=['delete'])
    def delete(self, request, username=None):
        # below would be great for user to remove its own account
        # username = request.user.username
        User.objects.filter(username=username).delete()
        return Response({'{}'.format(username): 'Successfully removed'})


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProgress(APIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        try:
            queryset = Translation.objects.filter(owner=user)
            serializer = TranslationSerializers(queryset, many=True)
            content = {
                # `django.contrib.auth.User` instance.
                'user': str(request.user),
                'auth': str(request.auth),  # None,
                'user_answered_correctly': serializer.data
            }
            return Response(content)
        except Translation.DoesNotExist:
            error_msg = 'Language object does not'
            ' exist for user {}'.format(user)
            error = {
                'error': error_msg}
            return Response(error)

    def put(self, request, format=None):
        ''' Update a list of translation for which user known the answer '''
        user = request.user
        data = request.data
        # if those lists have pks that are not in the database,
        # those additional pks will be ignored
        user_know_ids = data['user_know_ids']
        user_not_know_ids = data['user_not_know_ids']

        # add user to translation object
        translations = Translation.objects.filter(pk__in=user_know_ids)
        for translation in translations:
            translation.owner.add(user)
            translation.save()

        # remove user from translation object
        translations = Translation.objects.filter(pk__in=user_not_know_ids)
        for translation in translations:
            translation.owner.remove(user)
            translation.save()

        return Response({'STATUS': 'correctly_answered_list successfully updated'})


class isUser(APIView):
    def get(self, request, username):
        try:
            User.objects.get(username=username)
            return Response({'{}'.format(username): 'True'})
        except User.DoesNotExist:
            return Response({'{}'.format(username): 'False'})
