from django.db import models
from django.db.models.fields import IntegerField
from django.db.utils import IntegrityError


class Language(models.Model):
    conversion = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return self.conversion


class Translation(models.Model):
    translation = models.ForeignKey(
        Language, related_name='translations', on_delete=models.CASCADE)
    i = IntegerField()
    frontCard = models.CharField(max_length=20)
    backCard = models.CharField(max_length=20)
    target_language = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Translations'

    def __str__(self):
        new_dict = {'frontCard': self.frontCard,
                    'backCard': self.backCard}
        return str(new_dict)


def populate_db():
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
        print('"{}" key already exist. Skipping creation of Language instance'.format(
            conversion))
        print('#############')
        pass

    for translation in translations:
        language_obj = Language.objects.filter(
            conversion__contains=conversion)[0]
        i = translation['id']
        frontCard = translation['frontCard']
        backCard = translation['backCard']
        target_language = translation['target_language']

        if not Translation.objects.filter(translation_id=conversion,
                                          frontCard=frontCard):
            Translation.objects.create(
                translation=language_obj,
                i=i,
                frontCard=frontCard,
                backCard=backCard,
                target_language=target_language)


def get_latest_id(language):
    filtered = Translation.objects.filter(translation_id=language)
    latest_id = len(filtered)
    return latest_id


if __name__ == '__main__':
    populate_db()
