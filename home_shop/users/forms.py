from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    # error_messages = {
    #     'invalid_login': _(
    #         "Неверное имя пользователя или пароль."
    #     ),
    #     'inactive': _("Этот аккаунт отключён."),
    # }

    class Meta:
        model = User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')

    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
