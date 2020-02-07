from django import forms
from polls.models import UserProfileInfo
from polls.models import Plants
from polls.models import Water, NDVIMeasurement

from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

## Delete after
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class PlantsForm(forms.ModelForm):
    class Meta:
        model = Plants
        fields = ('deviceid', 'nickname', 'plant_pic')

class WaterForm(forms.ModelForm):
    class Meta:
        model = Water
        fields = ('WaterAdded',)

class NDVIForm(forms.ModelForm):
    class Meta:
        model = NDVIMeasurement
        fields = ('NDVI_value',)

    