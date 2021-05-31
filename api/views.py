from django.views.generic import TemplateView
from django.http import JsonResponse

from .models import Translation
from .serializers import TranslationSerializers, UserSerializer, GroupSerializer

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.


class APIGetTranslations(TemplateView):
    model = Translation

    def get(self, request):
        translation = Translation.objects.all()
        serializer = TranslationSerializers(translation, many=True)
        new_dict = {}
        new_dict['questions'] = serializer.data
        return JsonResponse(new_dict,
                            safe=False,
                            json_dumps_params={'indent': 4})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
