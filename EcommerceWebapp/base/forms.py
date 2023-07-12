from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Brand, Product


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_no', 'address', 'user_type']
        

class BrandForm(ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if self.owner:
            self.instance.owner = self.owner


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

