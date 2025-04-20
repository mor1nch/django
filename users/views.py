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
from users.services import reset_user_password


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
            success, message = reset_user_password(email)

            if success:
                messages.success(request, message)
                return redirect('login')

            messages.error(request, message)

        return render(request, 'password_reset.html', {'form': form})
