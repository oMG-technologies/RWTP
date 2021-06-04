from random_word import RandomWords


class WordsTranslation():
    def __init__(self, target_language='pl'):
        self.rw = RandomWords()
        self.target_language = target_language

    def get_random_words_n(self, n=10):
        random_words = []
        for _ in range(n):
            is_correct_word = False
            while is_correct_word is False:
                word = self.rw.get_random_word(hasDictionaryDef=True)
                if word is not None:
                    random_words.append(word)
        return random_words

    def get_random_words(self):
        is_correct = False
        while is_correct is False:
            random_words = self.rw.get_random_words(hasDictionaryDef=True)
            if random_words is not None:
                is_correct = True
                return random_words

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
        json_dict['questions'] = self.collect_questions()
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
        return translation_dict


if __name__ == '__main__':
    WordsTranslation(target_language='de').create_json()
# WordsTranslation().translate_text('pl', 'paralyze')
