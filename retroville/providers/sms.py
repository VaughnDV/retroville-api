from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SmsResult:
    ok: bool
    message: str


class SmsProvider(Protocol):
    def start_verification(self, phone_number: str, country_code: str) -> SmsResult: ...

    def check_verification(self, phone_number: str, country_code: str, code: str) -> SmsResult: ...


class FakeSmsProvider:
    """Offline demo/test double. Accepts code 1234."""

    def start_verification(self, phone_number: str, country_code: str) -> SmsResult:
        if not phone_number or not country_code:
            return SmsResult(False, "phone_number and country_code are required")
        return SmsResult(True, "Verification code sent")

    def check_verification(self, phone_number: str, country_code: str, code: str) -> SmsResult:
        if code == "1234":
            return SmsResult(True, "Phone verified")
        return SmsResult(False, "Invalid verification code")


class TwilioVerifyProvider:
    def __init__(self, account_sid: str, auth_token: str, service_sid: str):
        from twilio.rest import Client

        self._client = Client(account_sid, auth_token)
        self._service_sid = service_sid

    def start_verification(self, phone_number: str, country_code: str) -> SmsResult:
        to = f"+{country_code.lstrip('+')}{phone_number}"
        try:
            self._client.verify.v2.services(self._service_sid).verifications.create(to=to, channel="sms")
            return SmsResult(True, "Verification code sent")
        except Exception as exc:  # pragma: no cover - network failure path
            return SmsResult(False, str(exc))

    def check_verification(self, phone_number: str, country_code: str, code: str) -> SmsResult:
        to = f"+{country_code.lstrip('+')}{phone_number}"
        try:
            check = self._client.verify.v2.services(self._service_sid).verification_checks.create(
                to=to, code=code
            )
            if check.status == "approved":
                return SmsResult(True, "Phone verified")
            return SmsResult(False, check.status or "denied")
        except Exception as exc:  # pragma: no cover
            return SmsResult(False, str(exc))


def get_sms_provider() -> SmsProvider:
    from django.conf import settings

    if getattr(settings, "PROVIDERS_USE_FAKES", True) or not settings.TWILIO_VERIFY_SERVICE_SID:
        return FakeSmsProvider()
    return TwilioVerifyProvider(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_API_KEY_SECRET,
        settings.TWILIO_VERIFY_SERVICE_SID,
    )
