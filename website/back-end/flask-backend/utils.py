from datetime import datetime

import jwt
import requests
from jwt import ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidTokenError

from dictionary import API_AUDIENCE, AUTH0_JWKS_URL, AUTH0_DOMAIN

def validate_token(token):
    try:
        # Standard JWT validation
        # , get_public_key, algorithms=['RS256'] .... # add later from Oauth, public key
        decoded_token = jwt.decode(token,
                                   options={"verify_signature": False})  # Signature verification will be done later

        print(decoded_token)
        # Verify audience claims
        target_api_identifier = API_AUDIENCE
        if isinstance(decoded_token['aud'], str):
            print(decoded_token['aud'], target_api_identifier)
            if decoded_token['aud'] != target_api_identifier:
                return False, 'Invalid audience'
        elif isinstance(decoded_token['aud'], list):
            if target_api_identifier not in decoded_token['aud']:
                return False, 'Invalid audience'

        # Verify permissions (scopes)
        required_scopes = ['read:current_user']
        if 'scope' not in decoded_token:
            return False, 'Missing scope claim'
        token_scopes = decoded_token['scope'].split()
        for scope in required_scopes:
            if scope not in token_scopes:
                return False, f'Missing required scope: {scope}'

        if 'exp' in decoded_token:
            expiration_time = datetime.fromtimestamp(decoded_token['exp'])
            current_time = datetime.utcnow()
            if current_time > expiration_time:
                return False, 'Token has expired'

        return True, 'Token is valid'

    except ExpiredSignatureError:
        return False, 'Token has expired'
    except (InvalidIssuerError, InvalidAudienceError, InvalidTokenError):
        return False, 'Invalid token'