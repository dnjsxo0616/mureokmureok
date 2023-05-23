from django import forms
from .models import Supply

class SupplyForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(choices=Supply.tag_choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Supply
        fields = ('product_name', 'category', 'like', 'price', )

