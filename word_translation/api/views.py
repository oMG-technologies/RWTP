from django.views.generic import TemplateView
from django.http import JsonResponse

from .models import Translation
from .serializers import TranslationSerializers

# Create your views here.


class APIGetTranslations(TemplateView):
    model = Translation

    def get(self, request):
        translation = Translation.objects.all()
        serializer = TranslationSerializers(translation, many=True)
        return JsonResponse(serializer.data,
                            safe=False,
                            json_dumps_params={'indent': 4})
