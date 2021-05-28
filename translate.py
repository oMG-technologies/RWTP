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


random_words = WordsTranslation().get_random_words()
print(random_words)
