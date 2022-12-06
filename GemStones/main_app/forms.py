from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 
 
class createofferform(ModelForm):
    class Meta:
        model=offer
        fields="__all__"
        exclude=['status']
 
class createproductform(ModelForm):
    class Meta:
        model=Product
        fields='__all__'
 
class createbuyerform(ModelForm):
    class Meta:
        model=Buyer
        fields='__all__'
        exclude=['user']