from random_words import RandomWords
from typing import List, Dict


class WordsTranslation():
    def __init__(self, target_language='pl', count=2):
        self.rw = RandomWords()
        self.target_language = target_language
        self.count = count

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
            {'translatedText': 'wzgórze', 'detectedSourceLanguage': 'en', 'input': 'hill'}

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
        return result

    def create_json(self) -> None:
        '''Create a db.json file which will be used to populate DB '''
        import json
        json_dict = {}
        json_dict['conversion'] = 'en-{}'.format(self.target_language)
        json_dict['translations'] = self.collect_questions()
        with open('db.json', 'w+') as f:
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
            word: str) -> Dict[str, str]:
        ''' Create an inner dictionary with info about id, frontCard,
        backCard and target_language

        Parameters
        ----------
        id : int
            unique integer id
        word : str
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
        translation = self.translate_text(word)
        translated_word = translation['translatedText']

        # update dict
        translation_dict['id'] = id + 1
        translation_dict['frontCard'] = word
        translation_dict['backCard'] = translated_word
        translation_dict['target_language'] = self.target_language
        return translation_dict


if __name__ == '__main__':
    # languages_list = ['pl', 'de', 'fr, 'es', 'ru', 'it', 'sv', 'zh', '']
    WordsTranslation(target_language='zh', count=50).create_json()
