
from django.db import models
from django.db.models.fields import IntegerField
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


class Language(models.Model):
    ''' Create Language model '''
    conversion = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return self.conversion


class Translation(models.Model):
    ''' Create Translation model and link translation field to Language model
    Many-to-one relationship '''

    translation = models.ForeignKey(
        Language, related_name='translations', on_delete=models.CASCADE)
    i = IntegerField()
    frontCard = models.CharField(max_length=40)
    backCard = models.CharField(max_length=40)
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    pronunciation_frontCard = models.CharField(max_length=200)
    pronunciation_backCard = models.CharField(max_length=200)

    owner = models.ManyToManyField(
        User,
        related_name='owner',
        null=True)

    class Meta:
        verbose_name_plural = 'Translations'

    def __str__(self):
        new_dict = {'frontCard': self.frontCard,
                    'backCard': self.backCard}
        return str(new_dict)


# class Seen(models.Model):

#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='user')
#     language = models.ForeignKey(
#         Language, on_delete=models.CASCADE, related_name='language')
#     translation = models.ForeignKey(
#         Translation, on_delete=models.CASCADE)
#     known = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username


def populate_db() -> None:
    ''' Populate DataBase using db.json file '''

    import os
    import json

    json_path = os.path.join(os.getcwd(), 'db.json')
    with open(os.path.join(json_path), 'r') as f:
        data = json.load(f)
    translations = data['translations']
    conversion = data['conversion']
    try:
        Language.objects.create(
            conversion=conversion,
        )
    except IntegrityError:
        print('#############')
        print('#  WARNING  #')
        print('"{}" key already exist. Skipping creation of '
              'Language instance'.format(conversion))
        print('#############')

    for translation in translations:
        language_obj = Language.objects.filter(
            conversion__contains=conversion)[0]
        i = translation['id']
        frontCard = translation['frontCard']
        backCard = translation['backCard']
        pronunciation_frontCard = translation['pronunciation_frontCard']
        pronunciation_backCard = translation['pronunciation_backCard']
        target_language = translation['target_language']
        source_language = translation['source_language']

        # make sure duplicates will not be generated
        if not Translation.objects.filter(translation_id=conversion,
                                          frontCard=frontCard):
            Translation.objects.create(
                translation=language_obj,
                i=i,
                frontCard=frontCard,
                backCard=backCard,
                pronunciation_frontCard=pronunciation_frontCard,
                pronunciation_backCard=pronunciation_backCard,
                source_language=source_language,
                target_language=target_language,
            )


if __name__ == '__main__':
    populate_db()
