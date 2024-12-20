from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from users.models import EmailVerification, User
from users.utils import send_verification_email


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
            send_verification_email(user)

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
