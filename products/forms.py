# products/forms.py
from django import forms
from .models import Product, ProductAttribute, Category, Brand

class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'brand', 'image', 'stock_quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'stock_quantity': forms.NumberInput(),
        }

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['name', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Color'}),
            'value': forms.TextInput(attrs={'placeholder': 'e.g., Red'}),
        }
    # Use formset for multiple attributes