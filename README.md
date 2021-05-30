# RND_WORDS_Translation

An API for getting translation of random english words to a language of choise.

# REST API - list of endpoints

The root url:

`url = https://words-translation.herokuapp.com`

List of endpoints

| endpoint        |                feature                | method |
| --------------- | :-----------------------------------: | -----: |
| `\translations` | get 50 random words with translations |  `GET` |

# Quicktest

To quickly test the server respons, try this:

````bash
curl -H 'Accept: application/json; indent=4' https://words-translation.herokuapp.com/translations/```
````

You should receive a response like that

```bash
[
    {
        "i": 1,
        "frontCard": "proctors",
        "backCard": "opiekunowie"
    },
    {
        "i": 2,
        "frontCard": "museum",
        "backCard": "muzeum"
    },
    ...
    {
        ...
    },
    ...
    {
        "i": 50,
        "frontCard": "diamond-cutter",
        "backCard": "przecinak diamentowy"
    }
]
```
