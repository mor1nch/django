import string
from random import choice

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from skypro_online_store import settings
from users.models import User


def generate_random_password(length=8):
    """Генерирует случайный пароль заданной длины."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(characters) for _ in range(length))


def reset_user_password(email):
    try:
        user = User.objects.get(email=email)
        new_password = generate_random_password()
        user.password = make_password(new_password)
        user.save()

        send_mail(
            subject='Ваш новый пароль',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return True, 'Новый пароль был отправлен на ваш email.'
    except User.DoesNotExist:
        return False, 'Пользователь с таким email не найден.'
