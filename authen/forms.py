from django import forms
from django.core import validators

from authen.models import User


class RegisterForm(forms.Form):
  username = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'class': 'username-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Username',
      }
    ),
  )
  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={
        'class': 'email-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Email',
      }
    ),
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        'class': 'password-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Password',
      }
    ),
  )
  confirm_password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        'class': 'confirm-password-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Confirm Password',
      }
    ),
  )

  def clean(self):
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')
    confirm_password = self.cleaned_data.get('confirm_password')
    if User.objects.filter(email=email):
      print('hit email exits')
      raise forms.ValidationError("Email Existed!")
    if not password == confirm_password:
      print('hit validate')
      raise forms.ValidationError("Confirm Password not match password!")
    return confirm_password


class LoginForm(forms.Form):
  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={
        'class': 'email-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Email',
      }
    ),
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        'class': 'password-input-field w-full px-3 text-xl font-Primary-bold placeholder-slate-400 rounded-2xl bg-white border-4 border-slate-300',
        'placeholder': 'Password',
      }
    ),
  )

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if not User.objects.filter(email=email):
      raise forms.ValidationError("Account Not Existed!")
    return email
