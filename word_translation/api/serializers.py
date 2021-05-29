from rest_framework import serializers
from .models import Translation


class TranslationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['episode_number', 'date_published', 'link_to_mp3',
                  'link_to_podcast', 'idd', 'status', 'text']
