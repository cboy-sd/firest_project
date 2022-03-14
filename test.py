import os
from django.contrib.auth.password_validation import validate_password
import django.conf.global_settings

from django.test import TestCase
import dotenv

dotenv.read_dotenv()


class TryDjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        # SECRET_KEY = 'abc123'
        # self.assertEqual(SECRET_KEY=='abc123')

        try:
            # print(SECRET_KEY)
            validate_password(SECRET_KEY)
            self.fail()
        except AssertionError:
            print("the system called self.fail()")
        except Exception as e:
            msg = f'bad secret key  {e}'
            # print(msg)
            self.assertEqual(
                msg,
                "bad secret key  ['This password is too short. It must contain at least 8 characters.']"
            )
