from django import forms
from .models import FoodItem
from .models import CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['food', 'quantity']

from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'image']
