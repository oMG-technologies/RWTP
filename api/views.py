from django.views.generic import TemplateView
from django.http import JsonResponse

from .models import Translation, Language
from .serializers import (TranslationSerializers, UserSerializer,
                          GroupSerializer, LanguageSerializers, SingleTranslationSerializers)

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions

# Create your views here.


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


class SingleTranslation(TemplateView):

    model = Language

    def get(self, request, language):
        # episode = Language.objects.get(translation_id=language)
        episode = Language.objects.get(conversion='en-pl')
        serializer = TranslationSerializers(episode)
        return JsonResponse(serializer.data,
                            safe=False,
                            json_dumps_params={'indent': 4})


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
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Translation.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(translation_id=username)
            # queryset = queryset.filter(purchaser__username=username)
        return queryset

    # def get_queryset(self):
    #     user = self.kwargs['username']

    #     return Translation.objects.filter(translation_id=user)

        # def list(self, request, *args, **kwargs):
        #     param = request.GET.get('param')
        #     print(param)
        # queryset = Translation.objects.filter(translation_id='en-pl')
        # serializer_class = SingleTranslationSerializers


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
