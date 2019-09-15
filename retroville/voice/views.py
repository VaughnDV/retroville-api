import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authy.api import AuthyApiClient
from django.db.models import Q
from django.contrib.auth import get_user_model


User = get_user_model()


AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
PUSH_CREDENTIAL_SID = os.getenv("PUSH_CREDENTIAL_SID")
APP_SID = os.getenv("APP_SID")

api = AuthyApiClient(AUTHY_API_KEY)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def place_call(request):
    """
    Makes a call to the specified client using the Twilio REST API.
    """
    client = Client(API_KEY, API_KEY_SECRET, ACCOUNT_SID)
    if request.method == 'GET':
        to = request.GET["to"]
        caller = request.GET["From"]
    else:
        to = request.POST["to"]
        caller = request.GET["From"]

    call = client.calls.create(
        url=request.url_root + "incoming", to="client:" + to, from_=caller
    )

    return HttpResponse(str(call))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def make_call(request):
    """
    Creates an endpoint that can be used in your TwiML App as the Voice Request Url.
    In order to make an outgoing call using Twilio Voice SDK, you need to provide a
    TwiML App SID in the Access Token. You can run your server, make it publicly
    accessible and use `/makeCall` endpoint as the Voice Request Url in your TwiML App.
    """
    resp = VoiceResponse()
    if request.method == 'POST':
        to = request.POST.get("to")
        caller = request.POST.get("From")
    else:
        to = request.GET.get("to")
        caller = request.GET.get("From")

    resp.dial(callerId=caller, answer_on_bridge=True).client(to)

    return HttpResponse(str(resp))


@csrf_exempt
@require_http_methods(["GET", "POST"])
def ping(request):
    resp = VoiceResponse()
    resp.say("Pong!!")
    return HttpResponse(str(resp))


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
@require_http_methods(["POST"])
def send_sms(request):
    country_code = request.GET.get("country_code")
    phone_number = request.GET.get("phone_number")

    if not User.objects.filter(Q(country_code=country_code) and Q(phone_number=phone_number)):

        r = api.phones.verification_start(
            phone_number=phone_number,
            country_code=country_code,
            via='sms')

        if r.ok():
            return JsonResponse(data={
                "success": True,
                "message": r.content['message']
            })
        else:
            return JsonResponse(data={
                "success": False,
                "message": r.errors()['message']
            })
    return JsonResponse(data={
        "success": True,
        "message": "There is an account already associated with this number, please log in."
    })


@csrf_exempt
@require_http_methods(["POST"])
def validate_sms(request):
    country_code = request.GET.get("country_code")
    phone_number = request.GET.get("phone_number")
    code = request.GET.get("verification_code")

    r = api.phones.verification_check(phone_number, country_code, code)

    if r.ok():
        return JsonResponse(data={
            "success": True,
            "message": r.content['message']
        })
    else:
        return JsonResponse(data={
            "success": False,
            "message": r.errors()['message']
        })

