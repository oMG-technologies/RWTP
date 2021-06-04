from django.db import models
from django.db.models.fields import IntegerField

# Create your models here.


class Language(models.Model):
    language = models.CharField(max_length=6)


class Translation(models.Model):
    translation = models.ForeignKey(
        Language, related_name='translations', on_delete=models.CASCADE)
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
    Language.objects.create(
        language=language,
    )
    for translation in translations:
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
