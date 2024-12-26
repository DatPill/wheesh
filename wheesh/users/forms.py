from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
    UserCreationForm,
)
from users.models import User
from users.utils import (
    create_verification_object,
    email_verification_service,
    generate_verification_code,
)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    def save(self, commit = True, is_final = True):
        user =  super().save(commit=True)

        if is_final:  # TODO: fix double form saving in users.views.UserRegistrationView.form_valid
            code = generate_verification_code()
            create_verification_object(user.id, code)

            email_verification_service.send_verification_web(user.id, user.email, user.username, code)

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'profilePicInput', 'onchange': 'previewImage(event)'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-readonly form-control', 'id': 'disabledTextInput', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-readonly form-control', 'id': 'disabledTextInput', 'readonly': True}))


    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес эл. почты'}))

class UserSetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль', 'autocomplete': False}), label='Введите новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль', 'autocomplete': False}), label='Повторите новый пароль')
