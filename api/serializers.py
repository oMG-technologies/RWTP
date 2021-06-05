from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Translation, Language


class TranslationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = ['id',
                  'frontCard',
                  'backCard',
                  'target_language'
                  ]
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _id = data['id']
        frontCard = data['frontCard']
        backCard = data['backCard']
        target_language = data['target_language']
        updated_data = {'id': _id,
                        'frontCard': frontCard,
                        'backCard': backCard,
                        'target_language': target_language}
        return updated_data


class SingleTranslationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['frontCard',
                  'backCard',
                  'target_language'
                  ]


class LanguageSerializers(serializers.ModelSerializer):

    # lang = serializers.StringRelatedField(many=True)
    translations = TranslationSerializers(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ['conversion', 'translations']
        depth = 3


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
