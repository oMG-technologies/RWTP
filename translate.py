from random_word import RandomWords


class WordsTranslation():
    def __init__(self):
        self.rw = RandomWords()

    def get_random_words_n(self, n=10):
        random_words = []
        for _ in range(n):
            is_correct_word = False
            while is_correct_word is False:
                word = rw.get_random_word(hasDictionaryDef=True)
                if word is not None:
                    is_correct_word = True
                    random_words.append(word)
        return random_words

    def get_random_words(self):
        is_correct = False
        while is_correct is False:
            random_words = self.rw.get_random_words(hasDictionaryDef=True)
            if random_words is not None:
                is_correct = True
                return random_words

    def translate_text(self, target, text):
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        import six
        from google.cloud import translate_v2 as translate

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=target)

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(
            result["detectedSourceLanguage"]))


# random_words = WordsTranslation().get_random_words()
WordsTranslation().translate_text('pl', 'play')
# print(random_words)
