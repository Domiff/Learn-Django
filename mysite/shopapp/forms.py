from django import forms
from django.forms import FileInput, ClearableFileInput

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "preview",
        )

    FileInput.allow_multiple_selected = True
    images = forms.ImageField(
        widget=ClearableFileInput(),
    )


class CSVForm(forms.Form):
    csv_file = forms.FileField()
