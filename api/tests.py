from django.test import TestCase
import requests
import os


class APIResponseTestCaseGET(TestCase):

    def test_tranlations_endpoint_response(self):
        print('\n  ### Testing \'/translations endpoint\'')
        response = requests.get('http://127.0.0.1:8000/translations/')
        assert response.status_code == 200

    def test_single_tranlation_endpoint_response(self):
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

    def test_single_translation_endpoint_content(self):
        # languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        languages_list = ['pl']
        for language in languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            try:
                self.assertNotEqual(response.text, '[]')
            except AssertionError:
                print('    ! x={} test not passed'.format(language))
                raise AssertionError

    def test_single_translation_content_inner(self):
        # languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        languages_list = ['pl']
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

    def test_single_translation_content_inner_count(self):
        # languages_list = ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']
        languages_list = ['pl']
        for language in languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            if response.json():
                inner_dict = response.json()[0]
                n_inner_dict = len(inner_dict)
                self.assertEqual(n_inner_dict, 7)

    def test_language_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/language/')
        assert response.status_code == 200

    def test_available_conversion_endpoint_response(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        assert response.status_code == 200

    def test_available_conversion_endpoint_content(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        response_json = response.json()
        self.assertIn('available_conversions', response_json)

    def test_available_conversion_endpoint_content_inner(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        response_json = response.json()
        inner_dict = response_json['available_conversions'][0]
        keys = ['id', 'conversion', 'target_language_iso639',
                'target_language_iso3166', 'name']
        for key in keys:
            self.assertIn(key, inner_dict)

    def test_available_conversion_endpoint_content_inner_count(self):
        response = requests.get('http://127.0.0.1:8000/available_conversions/')
        response_json = response.json()
        inner_dict = response_json['available_conversions'][0]
        n_inner_dict = len(inner_dict)
        self.assertEqual(n_inner_dict, 5)


class APIResponseTestCasePOST(TestCase):

    @property
    def su(self):
        return os.environ['RWTP_su']

    @property
    def su_passwd(self):
        return os.environ['RWTP_su_passwd']


    def test_translations_endpoint_response_post_unauthenticated(self):
        example_input = {
            'translations': 'en-pl',
            "i": 1,
            "frontCard": "regulator",
            "backCard": "regulator",
            "pronunciation_frontCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625902264/en-US/regulator.mp3",
            "pronunciation_backCard": "http://res.cloudinary.com/hqzs7d3nl/raw/upload/v1625902265/pl/regulator.mp3",
            "source_language": "en-US",
            "target_language": "pl"
        }
        url = 'http://127.0.0.1:8000/translations/'
        response = requests.post(url, example_input)
        self.assertEqual(response.status_code, 403)

    def test_language_endpoint_response_post_unauthenticated(self):
        url = 'http://127.0.0.1:8000/language/'

        example = {
            "conversion": "en-pl"
        }

        response = requests.post(url, example)
        self.assertEqual(response.status_code, 403)

    def test_language_endpoint_response_post_authenticated(self):
        import os
        from requests.auth import HTTPBasicAuth
        url = 'http://127.0.0.1:8000/language/'

        example = {
            "conversion": "en-de"
        }
        su = os.environ['RWTP_su']
        su_passwd = os.environ['RWTP_su_passwd']

        response = requests.post(
            url, example, auth=HTTPBasicAuth(su, su_passwd))
        self.assertEqual(response.status_code, 201)


class APIResponseTestCaseDELETE(TestCase):

    @property
    def su(self):
        return os.environ['RWTP_su']

    @property
    def su_passwd(self):
        return os.environ['RWTP_su_passwd']

    def test_translation_endpoint_response_delete_authenticated(self):
        from requests.auth import HTTPBasicAuth
        url = 'http://127.0.0.1:8000/translations/12/remove/'
        response = requests.delete(
            url,
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))
        self.assertEqual(response.status_code, 200)

    def test_translation_endpoint_response_delete_unauthenticated(self):
        url = 'http://127.0.0.1:8000/translations/12/remove/'
        response = requests.delete(
            url,
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 403)

    def test_language_endpoint_response_delete_authenticated(self):
        from requests.auth import HTTPBasicAuth
        url = 'http://127.0.0.1:8000/language/en-de/remove/'

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))
        self.assertEqual(response.status_code, 200)

    def test_language_endpoint_response_delete_unauthenticated(self):
        url = 'http://127.0.0.1:8000/language/en-de/remove/'

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 403)
