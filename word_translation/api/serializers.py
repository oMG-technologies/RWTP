from rest_framework import serializers
from .models import Translation


class TranslationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = [
            'i',
            'frontCard',
            'backCard'
        ]
