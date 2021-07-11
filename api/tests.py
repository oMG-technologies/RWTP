from django.test import TestCase
import requests


class APIResponseTestCase(TestCase):
    def test_tranlations_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/translations/')
        assert response.status_code == 200

    def test_signle_tranlation_endpoint_response(self):
        languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        for language in languages_list:
            response = requests.get(
                'http://127.0.0.1:8000/translation/?conversion=en-{}/'.format(language))
            assert response.status_code == 200

    def test_all_single_translation_endpoint_content(self):
        languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        for language in languages_list:
            print(language)
            response = requests.get(
                'http://127.0.0.1:8000/translation/?conversion=en-{}/'.format(language))
            print(response.text)
            assert response.text != '[]'
            print('{} test passed'.format(language))

    def test_language_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/language/')
        assert response.status_code == 200

    def test_available_conversion_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        assert response.status_code == 200
