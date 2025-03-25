from django import forms


class ProductForm(forms.Form):
    name = forms.CharField(max_length=40)
    price = forms.DecimalField(min_value=1, max_value=1_000_000)
    description = forms.CharField(widget=forms.Textarea)
    
    