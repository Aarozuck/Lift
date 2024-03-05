from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Driver,Rider

class DriverRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    vehicle_type = forms.ChoiceField(choices=Driver.vehicle_choices)
    address = forms.ChoiceField(choices=Driver.address_choices)
    phone_number = forms.CharField(max_length=15)
    license_plate = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'vehicle_type', 'address', 'phone_number', 'license_plate']

class RiderRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'address', 'phone_number']


class UpdateDriverInfoForm(forms.Form):
    online_status = forms.ChoiceField(
        choices=(('online', 'Online'), ('offline', 'Offline')),
        required=True,
        widget=forms.RadioSelect
    )
    current_location = forms.CharField(max_length=100, required=True)
    # Other form fields as needed        


class RideRequestForm(forms.Form):
    current_location = forms.CharField(label='Current Location', max_length=100)
    destination = forms.CharField(label='Destination', max_length=100)    