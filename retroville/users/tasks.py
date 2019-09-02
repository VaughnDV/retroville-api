from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print("#" * 50)
    print("#" * 50)
    print("#" * 50)
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}"
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    print("#" * 50)
    print("#" * 50)
    print("#" * 50)
    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        'admin@retroville.com',
        [reset_password_token.user.email],
        fail_silently=False,
    )

    # msg = EmailMultiAlternatives(
    #     # title:
    #     "Password Reset for {title}".format(title="Some website title"),
    #     # message:
    #     email_plaintext_message,
    #     # from:
    #     "noreply@somehost.local",
    #     # to:
    #     [reset_password_token.user.email]
    # )
    # msg.attach_alternative(email_html_message, "text/html")
    # msg.send()
