[![Total alerts](https://img.shields.io/lgtm/alerts/g/mgierada/words_translation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mgierada/RWTP/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mgierada/RWTP.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mgierada/RWTP/context:python)

# RWTP

An API for getting translation of random english words to a language of choice together with the correct pronunciation.

# REST API - list of endpoints

The root url:

`base_url = https://words-translation.herokuapp.com`

List of endpoints

| endpoint                                                                                                  |                                                                                                                  feature                                                                                                                  | method |
| --------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | -----: |
| [`/translations`](https://words-translation.herokuapp.com/translations/)                                  |                                                                                 get 50 random English words with translations for all supported languages                                                                                 |  `GET` |
| [`/available_conversions/`](https://words-translation.herokuapp.com/available_conversions/)               | get all available conversions, i.e. translation from english `en` to various languages `x` in the `en-x` format. Currently, `x` can only be any of the following `pl`, `de`, `fr`, `es`, `ru`, `it`, `sv` and `zh`. More will come later. |  `GET` |
| [`/translation/?conversion=en-x/`](https://words-translation.herokuapp.com/translation/?conversion=en-pl) |                                      get 50 random English words with translations to a language `x`, which has to be in a [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) format                                      |  `GET` |
| [`/languages/`](http://127.0.0.1:8000/language/)                                                          |                                                               get 50 random English words and translations for all supported languages, categorized by language conversion                                                                |  `GET` |

# Quicktest

To quickly test the server respons, try this:

````bash
curl -H 'Accept: application/json; indent=4' https://words-translation.herokuapp.com/translations/```
````

You should receive a response like that

```bash
[
    {
        "id": 1,
        "frontCard": "adviser",
        "backCard": "doradca",
        "pronunciation_frontCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625904765/en-US/adviser.mp3",
        "pronunciation_backCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625904766/pl/doradca.mp3",
        "frontCard_language": "en-US",
        "backCard_language": "pl"
    },
    {
        "id": 2,
        "frontCard": "personality",
        "backCard": "osobowość",
        "pronunciation_frontCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625904767/en-US/personality.mp3",
        "pronunciation_backCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625904768/pl/osobowo%C5%9B%C4%87.mp3",
        "frontCard_language": "en-US",
        "backCard_language": "pl"
    },
    ...
    {
        ...
    }
    ...
]
```
