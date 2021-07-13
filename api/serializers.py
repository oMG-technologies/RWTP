from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Translation, Language
from typing import Dict


class TranslationSerializers(serializers.ModelSerializer):
    ''' Create TranslationSerializers to get a JSON response with translations
    for all available cnversions/languages'''

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
        ''' Modify representation appropriately

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


class TranslationDetailSerializers(serializers.ModelSerializer):
    # chapters = ChapterMarkSerializer(source='chaptermark_set', many=True)
    # media = MediaClipSerializer(source='mediaclip_set', many=True)
    # show = ShowSerializer()

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
        depth = 1
        # model = Episode
        # fields = ('url', 'id', 'title', 'subtitle', 'show', 'published_at', 'updated_at',
        #           'description', 'show_notes', 'cover_image', 'updated_at', 'chapters', 'media')
        # depth = 1


class SingleTranslationSerializers(serializers.ModelSerializer):
    ''' SingleTranslationSerializers to get a JSON Response with translations
    for a single conversion/language '''
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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ''' Create UserSerializer '''
    class Meta:
        model = User
        fields = ['url',
                  'username',
                  'email',
                  'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    ''' Create GroupSerializer '''
    class Meta:
        model = Group
        fields = ['url',
                  'name']
