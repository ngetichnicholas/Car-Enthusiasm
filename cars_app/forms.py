from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import User
from .models import *
from django.core.validators import MinLengthValidator,MaxLengthValidator


class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=("full_name","username","email","password1","password2")
        help_texts = {
            "username":None,
        }


class ContactForm(forms.ModelForm):
    class Meta:
      model = Contact
      fields = ['name','email','message']

class UpdateUserForm(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','full_name','email','phone','profile_picture','bio']