import re
from django.http import response
from django.test import TestCase
import requests
import os
import json


class APIResponseTestCase_01_GET(TestCase):
    print('# Testing GET requests #')

    @property
    def languages_list(self):
        return ['pl', 'de', 'fr', 'es', 'ru', 'it', 'sv', 'zh']

    @property
    def single_language(self):
        return ['pl']

    def test_tranlations_endpoint_response(self):
        print('\n  ### Testing \'/translations endpoint\'')
        response = requests.get('http://127.0.0.1:8000/translations/')
        assert response.status_code == 200

    def test_single_tranlation_endpoint_response(self):
        print('\n  ### Testing \'/translation/?conversion=en-x\' endpoint')

        for language in self.languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            try:
                assert response.status_code == 200
            except AssertionError:
                print('! {} test not passed'.format(language))
                raise AssertionError

    def test_single_translation_endpoint_content(self):

        for language in self.languages_list:
            url = 'http://127.0.0.1:8000/translation/?conversion=en-{}'.format(
                language)
            response = requests.get(url)
            try:
                self.assertNotEqual(response.text, '[]')
            except AssertionError:
                print('    ! x={} test not passed'.format(language))
                raise AssertionError

    def test_single_translation_content_inner(self):

        for language in self.languages_list:
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
        for language in self.languages_list:
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

    def test_is_user(self):
        basic_url = 'http://127.0.0.1:8000/is_user/'
        user = 'test_user'
        url = basic_url + user + '/'
        response = requests.get(url)
        print(response.text)
        assert response.status_code == 200


class APIResponseTestCase_02_POST(TestCase):
    print('# Testing POST requests #')

    @property
    def su(self):
        return os.environ['RWTP_su']

    @property
    def su_passwd(self):
        return os.environ['RWTP_su_passwd']

    def test_translations_endpoint_response_post_unauthenticated(self):
        example_input = {
            'conversion': 'en-pl',
            "i": 18,
            "frontCard": "some_word",
            "backCard": "some_translation",
            "pronunciation_frontCard": "here_will_be_the_link",
            "pronunciation_backCard": "here_will_be_the_link",
            "source_language": "en-US",
            "target_language": "pl"
        }
        url = 'http://127.0.0.1:8000/translations/18/post/'
        response = requests.post(
            url,
            data=json.dumps(example_input),
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 403)

    def test_translations_endpoint_response_post_authenticated(self):
        from requests.auth import HTTPBasicAuth
        example_input = {
            "i": 18,
            'conversion': 'en-pl',
            "frontCard": "some_word",
            "backCard": "some_translation",
            "pronunciation_frontCard": "here_will_be_the_link",
            "pronunciation_backCard": "here_will_be_the_link",
            "source_language": "en-US",
            "target_language": "pl"
        }
        url = 'http://127.0.0.1:8000/translations/18/post/'
        response = requests.post(
            url,
            data=json.dumps(example_input),
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))
        self.assertEqual(response.status_code, 200)

    def test_language_endpoint_response_post_unauthenticated(self):
        url = 'http://127.0.0.1:8000/language/'

        example = {
            "conversion": "en-pl"
        }

        response = requests.post(url, example)
        self.assertEqual(response.status_code, 403)

    def test_language_endpoint_response_post_authenticated(self):
        from requests.auth import HTTPBasicAuth
        url = 'http://127.0.0.1:8000/language/'

        example = {
            "conversion": "en-de"
        }

        response = requests.post(
            url,
            example,
            auth=HTTPBasicAuth(self.su, self.su_passwd))
        self.assertEqual(response.status_code, 201)


class APIResponseTestCase_03_DELETE(TestCase):
    print('# Testing DELETE requests #')

    @property
    def su(self):
        return os.environ['RWTP_su']

    @property
    def su_passwd(self):
        return os.environ['RWTP_su_passwd']

    def test_translation_endpoint_response_delete_authenticated(self):
        from requests.auth import HTTPBasicAuth

        response = requests.get('http://127.0.0.1:8000/translations/')
        data = response.json()[-1]
        current_id = data['id']

        url = 'http://127.0.0.1:8000/translations/{}/delete/'.format(
            current_id)

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))

        self.assertEqual(response.status_code, 200)

    def test_translation_endpoint_response_delete_unauthenticated(self):
        url = 'http://127.0.0.1:8000/translations/12/delete/'
        response = requests.delete(
            url,
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 403)

    def test_language_endpoint_response_delete_authenticated(self):
        from requests.auth import HTTPBasicAuth

        url = 'http://127.0.0.1:8000/language/en-de/delete/'

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))

        self.assertEqual(response.status_code, 200)

    def test_language_endpoint_response_delete_unauthenticated(self):
        url = 'http://127.0.0.1:8000/language/en-de/delete/'

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 403)

    def test_delete_user_by_superuser(self):
        from requests.auth import HTTPBasicAuth

        url = 'http://127.0.0.1:8000/user_remove/test_user/remove/'

        response = requests.delete(
            url,
            headers={'content-type': 'application/json'},
            auth=HTTPBasicAuth(self.su, self.su_passwd))
        print(response.text)

        self.assertEqual(response.status_code, 200)

    def test_delete_user_by_self(self):
        url_auth = 'http://127.0.0.1:8000/api-token-auth/'
        data = {
            "username": "test_user",
            "password": "test_password"
        }
        response_auth = requests.post(
            url_auth,
            data=json.dumps(data),
            headers={'content-type': 'application/json'})
        token = response_auth.json()['token']

        url = 'http://127.0.0.1:8000/user_remove/test_user/remove/'
        headers = {"Authorization": 'Token {}'.format(token)}
        response = requests.delete(
            url,
            headers=headers)
        print(response.text)

        self.assertEqual(response.status_code, 200)

    def test_delete_user_by_another_user(self):
        url_auth = 'http://127.0.0.1:8000/api-token-auth/'
        data = {
            "username": "test_user",
            "password": "test_password"
        }
        response_auth = requests.post(
            url_auth,
            data=json.dumps(data),
            headers={'content-type': 'application/json'})
        token = response_auth.json()['token']

        url = 'http://127.0.0.1:8000/user_remove/test_username/remove/'
        headers = {"Authorization": 'Token {}'.format(token)}
        response = requests.delete(
            url,
            headers=headers)
        print(response.text)

        self.assertEqual(
            response.text, '{"Error":"You are not authorized to remove this account"}')


class APIResponseTestCase_04_PUT(TestCase):
    print('# Testing PUT requests #')

    @ property
    def su(self):
        return os.environ['RWTP_su']

    @ property
    def su_passwd(self):
        return os.environ['RWTP_su_passwd']

    def test_add_new_user(self):
        url = 'http://127.0.0.1:8000/user_create/user/add/'
        example_input = {
            'username': 'test_user',
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "maciek.gierada@gmail.com",
            "password": "test_password",
        }
        response = requests.put(
            url,
            data=json.dumps(example_input),
            headers={'content-type': 'application/json'})
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_update_user_progress_user_know(self):
        url = 'http://127.0.0.1:8000/user_progress/'
        token = '5ed3bead9563b60924c30bbba4e2fc5a27473b32'
        headers = {'content-type': 'application/json',
                   "Authorization": 'Token {}'.format(token)}
        data = {'user_know_ids': [1, 2],
                'user_not_know_ids': []}
        response = requests.put(
            url,
            data=json.dumps(data),
            headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_update_user_progress_user_not_know(self):
        url = 'http://127.0.0.1:8000/user_progress/'
        token = '5ed3bead9563b60924c30bbba4e2fc5a27473b32'
        headers = {'content-type': 'application/json',
                   "Authorization": 'Token {}'.format(token)}
        data = {'user_know_ids': [],
                'user_not_know_ids': [1, 2]}
        response = requests.put(
            url,
            data=json.dumps(data),
            headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_update_user_progress_user_mix_POSknow_not_know(self):
        url = 'http://127.0.0.1:8000/user_progress/'
        token = '5ed3bead9563b60924c30bbba4e2fc5a27473b32'
        headers = {'content-type': 'application/json',
                   "Authorization": 'Token {}'.format(token)}
        data = {'user_know_ids': [1],
                'user_not_know_ids': [2]}
        response = requests.put(
            url,
            data=json.dumps(data),
            headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)


class APIResponseTestCase_05_AUTH(TestCase):
    print('# Testing AUTH requests #')

    def test_auth_token_generation(self):
        url = 'http://127.0.0.1:8000/api-token-auth/'
        data = {
            "username": "test_user",
            "password": "test_password"
        }
        response = requests.post(
            url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'})

        print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_token_validation(self):
        url = 'http://127.0.0.1:8000/user_progress/'
        token = '5ed3bead9563b60924c30bbba4e2fc5a27473b32'
        headers = {
            "Authorization": 'Token {}'.format(token)}
        response = requests.get(url, headers=headers)
        print(response.text)
        self.assertEqual(response.status_code, 200)
