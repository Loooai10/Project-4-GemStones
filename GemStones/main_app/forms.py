from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields  
from .models import UploadImage   
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 
 
class UserImage(ModelForm):  
    class meta:  
        # To specify the model to be used to create form  
        models = UploadImage  
        # It includes all the fields of model  
        fields = '__all__'  
class createofferform(ModelForm):
    class Meta:
        model= Offer
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