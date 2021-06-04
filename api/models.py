from django.db import models
from django.db.models.fields import IntegerField
from django.db.utils import IntegrityError

# Create your models here.


class Language(models.Model):
    language = models.CharField(max_length=6, primary_key=True)

    def __str__(self):
        return self.language


class Translation(models.Model):
    translation = models.ForeignKey(
        Language, related_name='translations', on_delete=models.CASCADE,)
    i = IntegerField()
    frontCard = models.CharField(max_length=20)
    backCard = models.CharField(max_length=20)

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
    language = data['language']
    try:
        Language.objects.create(
            language=language,
        )
    except IntegrityError:
        print('#############')
        print('#  WARNING  #')
        print('"{}" key already exist. Skipping creation of Language instance'.format(
            language))
        print('#############')
        pass

    for translation in translations:
        language = Language.objects.filter(language__contains=language)[0]
        i = translation['id']
        frontCard = translation['frontCard']
        backCard = translation['backCard']
        Translation.objects.create(
            translation=language,
            i=i,
            frontCard=frontCard,
            backCard=backCard
        )


#
populate_db()
