from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    CATEGORY_CHOICE = [
        ('화분', '화분'), ('실내식물', '실외식물'), ('관리상품', '관리상품'),
    ]

    category = forms.ChoiceField(
        label = '카테고리',
        widget=forms.Select(attrs={
            'class':'form-input',
            'id':'category',
            'placeholdeer':'분류',
        }),
        choices=CATEGORY_CHOICE,
    )

    class Meta:
        model = Product
        fields = ('title', 'content', 'category', 'price', 'photo',)