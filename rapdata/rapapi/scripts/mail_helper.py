import properties
from django.core.mail import send_mail

def send_email(subject, message, from_email, to_email):
    return send_mail(
        subject,
        message,
        from_email,
        [to_email],
        auth_user=properties.EMAIL_HOST_USER,
        auth_password=properties.EMAIL_HOST_PASSWORD,
        fail_silently=False,
    )
