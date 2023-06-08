from django import forms
from .models import Product, Review, Order

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


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs= {
                'class':'form-input',
                'placeholder' : '제목을 입력해주세요.',
            }
        ),

    )
    content = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs= {
                'class':'form-input',
                'placeholder' : '내용을 입력해주세요.',
            }
        ),
    )

    class Meta:
        model = Review
        fields = ('title', 'content',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_address', 'product_name', 'quantity', 'price')