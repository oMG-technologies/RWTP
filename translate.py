from random_words import RandomWords


class WordsTranslation():
    def __init__(self, target_language='pl', count=2):
        self.rw = RandomWords()
        self.target_language = target_language
        self.count = count

    def get_random_words(self):
        words = self.rw.random_words(count=self.count)
        return words

    def translate_text(self, text):
        ''' Translates text into the target language.

        Target must be an ISO 639-1 language code.

        See https://g.co/cloud/translate/v2/translate-reference#supported_languages

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

    def create_json(self):
        import json
        json_dict = {}
        json_dict['conversion'] = 'en-{}'.format(self.target_language)
        json_dict['translations'] = self.collect_questions()
        with open('db.json', 'w+') as f:
            json_string = json.dumps(json_dict, indent=4,
                                     ensure_ascii=False).encode('utf-8')
            f.write(json_string.decode())

    def collect_questions(self):
        questions = []
        for id, word in enumerate(self.get_random_words()):
            questions.append(self.create_inner_dict(id, word))
        return questions

    def create_inner_dict(self, id, word):
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
    languages_list = ['pl', 'du']
    WordsTranslation(target_language='pl', count=2).create_json()
    # l = WordsTranslation(target_language='de').get_random_words(10)
# WordsTranslation().translate_text('pl', 'paralyze')
