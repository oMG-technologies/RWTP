from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Translation, Language
from typing import Dict


class TranslationSerializers(serializers.ModelSerializer):
    ''' Create TranslationSerializers to get a JSON response with translations
    for all available conversions/languages'''

    class Meta:
        model = Translation
        fields = ['id',
                  'frontCard',
                  'backCard',
                  'pronunciation_frontCard',
                  'pronunciation_backCard',
                  'target_language',
                  'source_language',
                  ]
        depth = 3

    def to_representation(
            self,
            instance) -> Dict[str, str]:
        ''' Tune the server representation appropriately

        Returns
        -------
        Dict[str, str]
            a modified representation that will be displayed when called

        '''
        data = super().to_representation(instance)
        _id = data['id']
        frontCard = data['frontCard']
        backCard = data['backCard']
        pronunciation_frontCard = data['pronunciation_frontCard']
        pronunciation_backCard = data['pronunciation_backCard']
        target_language = data['target_language']
        source_language = data['source_language']
        updated_data = {'id': _id,
                        'frontCard': frontCard,
                        'backCard': backCard,
                        'pronunciation_frontCard': pronunciation_frontCard,
                        'pronunciation_backCard': pronunciation_backCard,
                        'frontCard_language': source_language,
                        'backCard_language': target_language,
                        }
        return updated_data


class SingleTranslationSerializers(serializers.ModelSerializer):
    ''' Create SingleTranslationSerializers to get a JSON response
    with translations for a single conversion/language '''
    class Meta:
        model = Translation
        fields = ['id',
                  'frontCard',
                  'backCard',
                  'pronunciation_frontCard',
                  'pronunciation_backCard',
                  'source_language',
                  'target_language',
                  ]


class LanguageSerializers(serializers.ModelSerializer):
    ''' Create LanguageSerializers '''

    translations = TranslationSerializers(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ['conversion',
                  'translations']
        depth = 3


class AvailableLanguagesSerializers(serializers.ModelSerializer):
    ''' Serializar to get an object with all available conversions '''
    class Meta:
        model = Language

        fields = ['conversion']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    ''' Create GroupSerializer '''
    class Meta:
        model = Group
        fields = ['url',
                  'name']
