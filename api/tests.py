from django.test import TestCase
import requests


class APIResponseTestCase(TestCase):
    def test_tranlations_endpoint_response(self):
        print('\n  ### Testing \'/translations endpoint\'')
        response = requests.get('http://127.0.0.1:8000/translations/')
        assert response.status_code == 200

    def test_signle_tranlation_endpoint_response(self):
        print('\n  ### Testing \'/translation/?conversion=en-x\' endpoint')
        languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        for language in languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            try:
                assert response.status_code == 200
            except AssertionError:
                print('! {} test not passed'.format(language))
                raise AssertionError

    # def test_single_translation_endpoint_content(self):
    #     languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
    #     for language in languages_list:
    #         url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
    #             language)
    #         response = requests.get(url)
    #         try:
    #             self.assertNotEqual(response.text, '[]')
    #         except AssertionError:
    #             print('    ! x={} test not passed'.format(language))
    #             raise AssertionError

    def test_single_translation_content_id(self):
        languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        for language in languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            if response.json():
                inner_dict = response.json()[0]
                keys = ['id', 'frontCard', 'backCard',
                        'pronunciation_frontCard', 'pronunciation_backCard',
                        'source_language', 'target_language']
                for key in keys:
                    self.assertIn(key, inner_dict)

    def test_language_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/language/')
        assert response.status_code == 200

    def test_available_conversion_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        assert response.status_code == 200
