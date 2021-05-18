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
    ("non" , "TravelType"),
    ("economy", "Economy"),
    ("business", "Buisness"),
    ("first", "First"),
)

class FlightForm(forms.Form):
    source = forms.CharField(max_length=40)
    destination = forms.CharField(max_length=40)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    travel_type = forms.ChoiceField(choices = CLASS)


class TrainForm(forms.Form):
    source = forms.CharField(max_length=40)
    destination = forms.CharField(max_length=40)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    travel_type = forms.ChoiceField(choices = CLASS)

HOTEL_TYPE = (
("3","3" ),
("5", "5" ),
("7" ,"7")

)
class HotelForm(forms.Form):
    location = forms.CharField(max_length=50)
    date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )
    number_of_days = forms.IntegerField(max_value=30 , min_value=1)
    hotel_type = forms.ChoiceField(choices = HOTEL_TYPE)


class UserPasswordResetForm(PasswordResetForm):
    def init(self, *args, **kwargs):
        super(UserPasswordResetForm, self).init(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'input is-medium is-rounded',
        'placeholder': 'Enter Email For Reset',
        'type': 'email',
        'name': 'email'
        }))

class BlogForm(forms.Form):
    blog_image = forms.ImageField(required=False)
    blog_heading = forms.CharField()
    blog_desc = forms.CharField(widget=forms.Textarea)
    blog_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
        , required=False
    )

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





