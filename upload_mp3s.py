import django
import cloudinary
import cloudinary.uploader
import cloudinary.api

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "word_translation.settings")

django.setup()


def upload():
    from api.models import Translation

    cloudinary.config(
        cloud_name=os.environ['cloudinary_CLOUD_NAME'],
        api_key=os.environ['cloudinary_API_KEY'],
        api_secret=os.environ['cloudinary_API_SECRET'],
        secure=True,
    )

    path_to_file = os.path.join(os.path.dirname(
        __file__), 'media', 'pl', '49_garsc.mp3')

    t = Translation.objects.get(backCard__contains='garść')
    t.save()
    print(t.pronunciation)


# def get_all
