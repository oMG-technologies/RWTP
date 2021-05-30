from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Translation


class TranslationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = ['i',
                  'frontCard',
                  'backCard'
                  ]
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_dict = {}
        new_dict['questions'] = data
        return new_dict

    # def to_representation(self, instance):
    #     response_dict = dict()
    #     response_dict['questions'] = {
    #     }
    #     return response_dict


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
