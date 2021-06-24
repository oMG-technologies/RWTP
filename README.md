[![Total alerts](https://img.shields.io/lgtm/alerts/g/mgierada/words_translation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mgierada/words_translation/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mgierada/words_translation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mgierada/words_translation/context:python)

# RND_WORDS_Translation

An API for getting translation of random english words to a language of choise.

# REST API - list of endpoints

The root url:

`base_url = https://words-translation.herokuapp.com`

List of endpoints

| endpoint                         |                                                                                                                  feature                                                                                                                  | method |
| -------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | -----: |
| `/translations`                  |                                                                                 get 50 random English words with translations for all supported languages                                                                                 |  `GET` |
| `/available_conversions/`        | get all available conversions, i.e. translation from english `en` to various languages `x` in the `en-x` format. Currently, `x` can only be any of the following `pl`, `de`, `fr`, `es`, `ru`, `it`, `sv` and `zh`. More will come later. |  `GET` |
| `/translation/?conversion=en-x/` |                                      get 50 random English words with translations to a language `x`, which has to be in a [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) format                                      |  `GET` |
| `/languages/`                    |                                                               get 50 random English words and translations for all supported languages, categorized by language conversion                                                                |  `GET` |

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
        "frontCard": "upside",
        "backCard": "do góry",
        "target_language": "pl"
    },
    {
        "id": 2,
        "frontCard": "bear",
        "backCard": "Niedźwiedź",
        "target_language": "pl"
    },
    ...
    {
        ...
    }
    ...
]
```
