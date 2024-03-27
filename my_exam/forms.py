from django import forms
from .models import User, Iphone
from django.core.validators import RegexValidator
import re


class LoginForm(forms.Form):
    mobile_or_email = forms.CharField(label='Phone або Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean_mobile_or_email(self):
        data = self.cleaned_data['mobile_or_email']
        if re.match(r'^[0-9]+$', data):
            return data
        elif re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data):
            return data
        else:
            raise forms.ValidationError('Phone або Email неправильного формату')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Підтвердіть пароль', widget=forms.PasswordInput)
    mobile = forms.CharField(label='Mobile', max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Мобільний номер телефону повинен бути в форматі: '+999999999'. Довжина не більше 15 символів.")])

    class Meta:
        model = User
        fields = ('first_name', 'age', 'email', 'password', 'confirm_password', 'mobile', 'address')


    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        return mobile

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають.')
        return confirm_password

    def save(self, commit=True):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValueError("Паролі не співпадають")
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class IphoneForm(forms.ModelForm):
    class Meta:
        model = Iphone
        fields = ['name', 'color', 'memory', 'price', 'image_url']