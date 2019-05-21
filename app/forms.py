from django import forms
from django.utils import timezone
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta(object):
        model = Order
        fields = ('first_name',
            'last_name',
            'phone',
            'address',
            'buying_type',
            'comment')

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