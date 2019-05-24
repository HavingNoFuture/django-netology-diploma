from django import forms
from django.utils import timezone
from .models import Order, Review
from django.contrib.auth.models import User


class OrderForm(forms.ModelForm):

    class Meta(object):
        model = Order
        fields = (
            'first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'comment'
        )

        labels = {
            'first_name': 'Ваше имя:',
            'last_name': 'Ваша фамилия:',
            'phone': 'Номер телефона:',
            'address': 'Адресс доставки:',
            'buying_type': 'Тип доставки:',
            'comment': 'Комментарий:',
        }

        help_texts = {
            'phone': 'Пожалуйста, укажите реальный номер телефона, по которому с Вами можно связаться',
            'address': '*Обязательно укажите адресс!'
        }


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput)
    password_check.label = 'Повторите пароль:'

    password = forms.CharField(widget=forms.PasswordInput)
    password.label = 'Пароль:'
    password.help_text = 'Придумайте пароль.'

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_check',
            'email',
            'first_name',
            'last_name',
        )

        labels = {
            'first_name': 'Имя:',
            'last_name': 'Фамилия:',
            'email': 'Email:',
            'username': 'Логин:',
        }

        help_texts = {
            'email': 'Пожалуйста, укзаывайте реальный адресс.',
        }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже существует!')

        if password != password_check:
            raise forms.ValidationError('Пароли не совпадают! Попробуйте снова!')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот Email уже занят другим пользователем!')


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    email.label = 'Email:'
    password.label= 'Пароль:'

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого Email нет в системе!')

        user = User.objects.get(email=email)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль!')


RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES)
    rating.label = 'Оцените:'

    class Meta(object):
        model = Review
        fields = (
            'text',
            'rating',
        )

        labels = {
            'text': 'Комментарий:',
        }
