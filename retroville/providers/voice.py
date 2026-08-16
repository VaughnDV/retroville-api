from __future__ import annotations

from typing import Protocol

from django.conf import settings


class VoiceProvider(Protocol):
    def access_token(self, identity: str) -> str: ...


class FakeVoiceProvider:
    def access_token(self, identity: str) -> str:
        return f"demo-token:{str(identity).replace('-', '_')}"


class TwilioVoiceProvider:
    def access_token(self, identity: str) -> str:
        from twilio.jwt.access_token import AccessToken
        from twilio.jwt.access_token.grants import VoiceGrant

        identity = str(identity).replace("-", "_")
        grant = VoiceGrant(
            push_credential_sid=settings.TWILIO_PUSH_CREDENTIAL_SID,
            outgoing_application_sid=settings.TWILIO_APP_SID,
        )
        token = AccessToken(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_API_KEY,
            settings.TWILIO_API_KEY_SECRET,
            identity=identity,
        )
        token.add_grant(grant)
        jwt = token.to_jwt()
        return jwt.decode() if isinstance(jwt, bytes) else str(jwt)


def get_voice_provider() -> VoiceProvider:
    from django.conf import settings

    if getattr(settings, "PROVIDERS_USE_FAKES", True):
        return FakeVoiceProvider()
    return TwilioVoiceProvider()
