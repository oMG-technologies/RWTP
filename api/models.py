from django.db import models
from django.db.models.fields import IntegerField
from django.db.utils import IntegrityError

# Create your models here.


class Language(models.Model):
    conversion = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return self.language


class Translation(models.Model):
    translation = models.ForeignKey(
        Language, related_name='translations', on_delete=models.CASCADE)
    i = IntegerField()
    frontCard = models.CharField(max_length=20)
    backCard = models.CharField(max_length=20)
    target_language = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Translation'

    def __str__(self):
        new_dict = {'id': self.i, 'frontCard': self.frontCard,
                    'backCard': self.backCard}
        return str(new_dict)


def populate_db():
    import os
    import json

    json_path = os.path.join(os.getcwd(), 'db.json')
    print(json_path)
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

    # print(Translation.objects.filter(translation_id='en-pl'))

    for translation in translations:
        language_obj = Language.objects.filter(
            conversion__contains=conversion)[0]
        i = translation['id']
        frontCard = translation['frontCard']
        backCard = translation['backCard']
        target_language = translation['target_language']

        # latest_id = get_latest_id(language)
        # print(latest_id)
        # if not Translation.objects.filter(translation_id='en-pl'):
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


#
# populate_db()
