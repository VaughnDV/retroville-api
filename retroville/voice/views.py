import os
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
PUSH_CREDENTIAL_SID = "CR***"
APP_SID = os.getenv("APP_SID")

"""
Use a valid Twilio number by adding to your account via https://www.twilio.com/console/phone-numbers/verified
"""
CALLER_NUMBER = "1234567890"

"""
The caller id used when a client is dialed.
"""
CALLER_ID = "client:quick_start"
IDENTITY = "alice"


@csrf_exempt
@require_http_methods(["GET", "POST"])
def token(request):
    """
    Creates an access token with VoiceGrant using your Twilio credentials.
    """
    account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
    api_key = os.environ.get("API_KEY", API_KEY)
    api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
    push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
    app_sid = os.environ.get("APP_SID", APP_SID)

    grant = VoiceGrant(
        push_credential_sid=push_credential_sid, outgoing_application_sid=app_sid
    )

    identity = (
        request.body["identity"]
        if request.body and request.body["identity"]
        else IDENTITY
    )
    token = AccessToken(account_sid, api_key, api_key_secret, identity=identity)
    token.add_grant(grant)

    return HttpResponse(token.to_jwt())


@csrf_exempt
@require_http_methods(["GET", "POST"])
def incoming(request):
    """
    Creates an endpoint that plays back a greeting.
    """
    resp = VoiceResponse()
    resp.say("Congratulations! You have received your first inbound call! Good bye.")
    return HttpResponse(str(resp))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def placeCall(request):
    """
    Makes a call to the specified client using the Twilio REST API.
    """
    account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
    api_key = os.environ.get("API_KEY", API_KEY)
    api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

    client = Client(api_key, api_key_secret, account_sid)
    to = request.body.get("to")
    call = None

    if to is None or len(to) == 0:
        call = client.calls.create(
            url=request.url_root + "incoming", to="client:" + IDENTITY, from_=CALLER_ID
        )
    elif to[0] in "+1234567890" and (len(to) == 1 or to[1:].isdigit()):
        call = client.calls.create(
            url=request.url_root + "incoming", to=to, from_=CALLER_NUMBER
        )
    else:
        call = client.calls.create(
            url=request.url_root + "incoming", to="client:" + to, from_=CALLER_ID
        )

    return HttpResponse(str(call))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def makeCall(request):
    """
    Creates an endpoint that can be used in your TwiML App as the Voice Request Url.
    In order to make an outgoing call using Twilio Voice SDK, you need to provide a
    TwiML App SID in the Access Token. You can run your server, make it publicly
    accessible and use `/makeCall` endpoint as the Voice Request Url in your TwiML App.
    """
    resp = VoiceResponse()
    to = request.body.get("to")

    if to is None or len(to) == 0:
        resp.say("Congratulations! You have just made your first call! Good bye.")
    elif to[0] in "+1234567890" and (len(to) == 1 or to[1:].isdigit()):
        resp.dial(callerId=CALLER_NUMBER).number(to)
    else:
        resp.dial(callerId=CALLER_ID).client(to)

    print(str(resp))
    return str(resp)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def ping(request):
    resp = VoiceResponse()
    resp.say("Pong!!")
    return HttpResponse(str(resp))
