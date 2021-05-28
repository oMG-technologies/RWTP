from random_word import RandomWords


def get_random_words(n=10):
    random_words = []
    not_corrected_words = []
    rw = RandomWords()
    for _ in range(n):
        is_correct_word = False
        while is_correct_word is False:
            word = rw.get_random_word(hasDictionaryDef=True)
            not_corrected_words.append(word)
            if word is not None:
                is_correct_word = True
                random_words.append(word)
    return random_words


random_words = get_random_words()
print(random_words)
