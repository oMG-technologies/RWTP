from django.views.generic import TemplateView

from .models import Translation

# Create your views here.


class APIGetTranslations(TemplateView):
    model = Tranlation

    def get(self, request):
        translation = Translation.objects.all()
        serializer = TranslationSerializers(translation, many=True)
        return JsonResponse(serializer.data,
                            safe=False,
                            json_dumps_params={'indent': 4})
