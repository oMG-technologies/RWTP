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
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _id = data['i']
        frontCard = data['frontCard']
        backCard = data['backCard']
        updated_data = {'id': _id,
                        'frontCard': frontCard,
                        'backCard': backCard}
        return updated_data


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
