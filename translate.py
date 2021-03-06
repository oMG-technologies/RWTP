from random_words import RandomWords
from typing import List, Dict
from text_to_speech import TextToSpeech
import os

import django
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.exceptions import Error

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "word_translation.settings")

django.setup()


class WordsTranslation():
    def __init__(self, target_language='pl', count=2):
        self.rw = RandomWords()
        self.target_language = target_language
        self.count = count
        self.tts = TextToSpeech()

    def get_random_words(self) -> List[str]:
        '''Get count ammount of random English words[summary]

        Returns
        -------
        List[str]
            a list with random english words. Use count parameter to set
            how many words a list should contain

        '''
        words = self.rw.random_words(count=self.count)
        return words

    def translate_text(
            self,
            text: str) -> Dict[str, str]:
        ''' Translate text into the target language.

        Target must be an ISO 639-1 language code.

        See https://g.co/cloud/translate/v2/translate-reference#supported_languages

        Parameters
        ----------
        text : str
            an English word to be translated

        Returns
        -------
        Dict[str, str]
            Server response in a python's dict format

            e.g.
            >>> WordsTranslation(target_language='pl', count=1).translate_text('hill')
            {'translatedText': 'wzgórze',
                'detectedSourceLanguage': 'en', 'input': 'hill'}

        '''
        import six
        from google.cloud import translate_v2 as translate

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.

        result = translate_client.translate(
            text, target_language=self.target_language)
        print('{} translation finshed with no errors'.format(text))
        return result

    def create_json(self) -> None:
        '''Create a db.json file which will be used to populate 
        a production DB '''

        import json
        json_dict = {}
        json_dict['conversion'] = 'en-{}'.format(self.target_language)
        json_dict['translations'] = self.collect_questions()
        path_to_db = os.path.join(os.path.dirname(__file__), 'db.json')
        with open(path_to_db, 'w+') as f:
            json_string = json.dumps(json_dict, indent=4,
                                     ensure_ascii=False).encode('utf-8')
            f.write(json_string.decode())

    def collect_questions(self) -> List[Dict[str, str]]:
        ''' A question list holding all Google Cloud Translate server responses

        Returns
        -------
        List[Dict[str, str]]
            a list having the following format:

            [
                {
                    "id": 1,
                    "frontCard": "buildings",
                    "backCard": "建筑物",
                    "target_language": "zh"
                },
                {
                    "id": 2,
                    "frontCard": "perforation",
                    "backCard": "穿孔",
                    "target_language": "zh"
                },
            ]

        '''
        questions = []
        for id, word in enumerate(self.get_random_words()):
            questions.append(self.create_inner_dict(id, word))
        return questions

    def create_inner_dict(
            self,
            id: int,
            frontCard: str) -> Dict[str, str]:
        ''' Create an inner dictionary with info about id, frontCard,
        backCard and target_language

        Parameters
        ----------
        id : int
            unique integer for each translated word
        frontCard : str
            a word to be translated

        Returns
        -------
        Dict[str, str]
            a dict of a following format:

            {
                "id": 1,
                "frontCard": "buildings",
                "backCard": "建筑物",
                "target_language": "zh"
            },

        '''
        translation_dict = {}
        translation_response = self.translate_text(frontCard)
        backCard = translation_response['translatedText']

        pronunciation_frontCard = self.get_pronunciation_link(
            id,
            frontCard,
            'en-US')

        pronunciation_backCard = self.get_pronunciation_link(
            id,
            backCard,
            self.target_language)

        # update translation_dict
        translation_dict['id'] = id + 1
        translation_dict['frontCard'] = frontCard
        translation_dict['backCard'] = backCard
        translation_dict['pronunciation_frontCard'] = pronunciation_frontCard
        translation_dict['pronunciation_backCard'] = pronunciation_backCard
        translation_dict['target_language'] = self.target_language
        translation_dict['source_language'] = 'en-US'

        return translation_dict

    def get_pronunciation_link(
            self,
            id: int,
            word: str,
            language_code: str) -> str:
        ''' Prepare input to get a link to uploaded .mp3 file (Cloudinary)

        Parameters
        ----------
        id : int
            unique integer for each translated word
        word : str
            an English word to be translated
        language_code : str
            the same code as the one used for translation - here just
            for organization of uploaded files
            e.g. 'en-US' or 'pl'

        Returns
        -------
        str
            link to Cloudinary uploaded .mp3 file

        '''
        path_to_pronunciation_word = self.tts.get_pronunciation(
            id, word, language_code)
        remote_folder = language_code + '/'
        pronunciation = self.upload_mp3(word,
                                        path_to_pronunciation_word,
                                        remote_folder)
        return pronunciation

    def upload_mp3(
            self,
            public_id: str,
            path_to_pronunciation_local: str,
            remote_folder: str) -> str:
        ''' Upload .mp3 file with correct pronunciation to Cloudinary

        Parameters
        ----------
        public_id : str
            a name for file stored in Couldinary
        path_to_pronunciation_local : str
            local path to .mp3 file
        remote_folder : str
            a name of the directory to store an uploaded /mp3 file

        Returns
        -------
        str
            link to Cloudinary uploaded .mp3 file

        '''
        # Specify cloudinary configuration
        cloudinary.config(
            cloud_name=os.environ['cloudinary_CLOUD_NAME'],
            api_key=os.environ['cloudinary_API_KEY'],
            api_secret=os.environ['cloudinary_API_SECRET'],
            secure=True,
        )
        # for some languages, the unicode cleaning of file name does not work
        # perfectly. In such cases, the public_id property would be a randomly
        # generated string
        try:
            response = cloudinary.uploader.upload(path_to_pronunciation_local,
                                                  folder=remote_folder,
                                                  public_id=public_id,
                                                  overwrite=True,
                                                  resource_type='raw')
        except Error:
            response = cloudinary.uploader.upload(path_to_pronunciation_local,
                                                  folder=remote_folder,
                                                  overwrite=True,
                                                  resource_type='raw')
        url = response['url']
        print('Link to audio content succesfully generated')
        return url


if __name__ == '__main__':
    # languages_list = ['pl', 'de', 'fr, 'es', 'ru', 'it', 'sv', 'zh']
    WordsTranslation(target_language='zh', count=50).create_json()
