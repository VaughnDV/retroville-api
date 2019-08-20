import os
import json
import ast
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant


ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
PUSH_CREDENTIAL_SID = os.getenv("PUSH_CREDENTIAL_SID")
APP_SID = os.getenv("APP_SID")


def generate_token(identity):
    """
    Creates an access token with VoiceGrant using Twilio credentials.
    """

    if "-" in identity:
        identity = identity.replace("-", "_")

    grant = VoiceGrant(
        push_credential_sid=PUSH_CREDENTIAL_SID, outgoing_application_sid=APP_SID
    )
    token = AccessToken(ACCOUNT_SID, API_KEY, API_KEY_SECRET, identity=identity)
    token.add_grant(grant)

    return str(token.to_jwt()).split("'")[1]
