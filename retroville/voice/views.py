from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from twilio.twiml.voice_response import VoiceResponse

from retroville.providers.sms import get_sms_provider
from retroville.users.models import User


@csrf_exempt
@require_http_methods(["GET", "POST"])
def place_call(request):
    return HttpResponse("Voice calling is disabled in the offline demo.", status=501)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def make_call(request):
    to = request.POST.get("to") or request.GET.get("to")
    caller = request.POST.get("From") or request.GET.get("From")
    resp = VoiceResponse()
    if to and caller:
        resp.dial(callerId=caller, answer_on_bridge=True).client(to)
    else:
        resp.say("Missing call parameters")
    return HttpResponse(str(resp), content_type="text/xml")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def ping(request):
    resp = VoiceResponse()
    resp.say("Pong!!")
    return HttpResponse(str(resp), content_type="text/xml")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def incoming(request):
    resp = VoiceResponse()
    resp.say("Congratulations! You have received your first inbound call! Good bye.")
    return HttpResponse(str(resp), content_type="text/xml")


@csrf_exempt
@require_http_methods(["POST"])
def send_sms(request):
    country_code = request.GET.get("country_code") or request.POST.get("country_code")
    phone_number = request.GET.get("phone_number") or request.POST.get("phone_number")
    if User.objects.filter(country_code=country_code, phone_number=phone_number).exists():
        return JsonResponse(
            {
                "success": True,
                "message": "There is an account already associated with this number, please log in.",
            }
        )
    result = get_sms_provider().start_verification(phone_number or "", country_code or "")
    return JsonResponse({"success": result.ok, "message": result.message})


@csrf_exempt
@require_http_methods(["POST"])
def validate_sms(request):
    country_code = request.GET.get("country_code") or request.POST.get("country_code")
    phone_number = request.GET.get("phone_number") or request.POST.get("phone_number")
    code = request.GET.get("verification_code") or request.POST.get("verification_code")
    result = get_sms_provider().check_verification(phone_number or "", country_code or "", code or "")
    return JsonResponse({"success": result.ok, "message": result.message})
