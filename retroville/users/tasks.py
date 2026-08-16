import logging

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created

logger = logging.getLogger(__name__)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = settings.PASSWORD_RESET_CONFIRM_URL.format(token=reset_password_token.key)
    context = {
        "email": reset_password_token.user.email,
        "reset_password_url": reset_url,
    }
    try:
        body = render_to_string("email/user_reset_password.txt", context)
    except Exception:
        body = f"Reset your password: {reset_url}"
    send_mail(
        "Password reset for Retroville",
        body,
        settings.DEFAULT_FROM_EMAIL,
        [reset_password_token.user.email],
        fail_silently=False,
    )
    logger.info("password_reset.sent", extra={"user_id": str(reset_password_token.user_id)})
