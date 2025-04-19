import string
from random import choice

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from skypro_online_store import settings
from users.forms import UserRegistrationForm, ResetPasswordForm
from users.models import User


def generate_random_password(length=8):
    """Генерирует случайный пароль заданной длины."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(characters) for _ in range(length))


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Здравствуйте! Вы успешно зарегистрировались!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return response


class ResetPasswordView(View):
    """Контроллер для восстановления пароля."""

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'password_reset.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                new_password = generate_random_password()
                user.password = make_password(new_password)
                user.save()

                # Отправка email с новым паролем
                send_mail(
                    subject='Ваш новый пароль',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Новый пароль был отправлен на ваш email.')
                return redirect('login')  # Перенаправление на страницу входа
            except User.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден.')

        return render(request, 'password_reset.html', {'form': form})
