# coding:utf-8
import datetime

from ..consts import _const
api_settings = _const()

SECRET_KEY = "F5XazmTEJKAugRJ0MHkLMlyfqMT3ts6SNXrbGnNTY1nzoW8uQ"

from secs.utils.jwt_auth.local_jwt.jwt_settings import JWT_AUTH as DJANGO_JWT_AUTH


JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}

DEFAULT_JWT_AUTH = JWT_AUTH
for x in DEFAULT_JWT_AUTH.keys():
    if x in DJANGO_JWT_AUTH.keys():
        JWT_AUTH[x] = DJANGO_JWT_AUTH[x]


for k, v in JWT_AUTH.items():
    api_settings.__setattr__(k, v)


USERNAME_FIELD = "username"
Authentication_KEY = 'Authorization'