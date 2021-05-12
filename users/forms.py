from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

CLASS =(
    ("economy", "Economy"),
    ("buisness", "Buisness"),
    ("first", "First"),
)

class FlightForm(forms.Form):
    source = forms.CharField(max_length=40)
    destination = forms.CharField(max_length=40)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    travel_type = forms.ChoiceField(choices = CLASS)


class UserPasswordResetForm(PasswordResetForm):
    def init(self, *args, **kwargs):
        super(UserPasswordResetForm, self).init(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'input is-medium is-rounded',
        'placeholder': 'Enter Email For Reset',
        'type': 'email',
        'name': 'email'
        }))

# class UserPasswordReset(PasswordChangeForm):
#     def init(self, *args, **kwargs):
#         super(PasswordChangeForm, self).init(*args, **kwargs)

#     password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
#         'class': 'input is-medium is-rounded',
#         'placeholder': '*************',
#         'type': 'password',
#         'name': 'password'
#         }))
#     pass = forms.CharField(label='', widget=forms.PasswordInput(attrs={
#         'class': 'input is-medium is-rounded',
#         'placeholder': '*************',
#         'type': 'password',
#         'name': 'password'
#         }))





