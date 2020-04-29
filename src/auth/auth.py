import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'kcemenike.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'kcemenike'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # Return 401 if authorization header does not exist
    if not auth:
        # print("No auth")
        raise AuthError({
            'code': 'no_auth_header',
            'description': 'Authorization header is missing. Kindly include'
        }, 401)
    # print(auth)
    if len(auth.split()) != 2:
        raise AuthError({
            'code': 'invalid_auth',
            'description': 'Authorization invalid, please try again'
        }, 401)
    elif auth.split()[0].lower() != 'bearer':
        raise AuthError({
            'code': 'no_bearer',
            'description': "Authorization header must start with 'Bearer'"
        }, 401)
    # print(auth.split())
    else:
        return auth.split()[1]
    raise AuthError({
        'code': 'invalid_auth',
        'description': 'Authorization invalid'
    })
    # raise Exception('Not Implemented')


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid claim',
            'description': 'please include permissions in token'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': "You are not authorized to perform this action"
        }, 403)

    return True

    # raise Exception('Not Implemented')


def verify_decode_jwt(token):
    url = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwt_keys = json.loads(url.read())

    unverified_header = jwt.get_unverified_header(token)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization invalid'
        }, 401)

    for key in jwt_keys['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {index: value for index, value in key.items() if index in [
                'kid', 'kty', 'use', 'n', 'e']}

    try:
        payload = jwt.decode(token=token, key=rsa_key, algorithms=ALGORITHMS,
                             audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/")
        return payload

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Claims invalid'
        }, 401)

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'expired_token',
            'description': 'This token has expired, please generate another toekn'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse token'
        }, 400)

    # final error catch
    raise AuthError({
        'code': 'invalid',
        'description': 'Key not found in token'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Token invalid, kindly try again with valid token'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
