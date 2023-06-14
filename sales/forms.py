from django import forms
from .models import Product, Review, Order
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField, TagWidget


class ProductForm(forms.ModelForm):
    title = forms.CharField(
        label='상품명',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '상품명',
                'placeholder': '상품명을 입력해주세요',
            }
        )
    )

    CATEGORY_CHOICE = [
        ('화분', '화분'), ('삽', '삽'), ('식물', '식물'), ('비료', '비료'), ('습도', '습도'), ('물주기', '물주기'), ('온도', '온도')
    ]

    category = forms.ChoiceField(
        label = '카테고리',
        widget=forms.Select(attrs={
            'class': 'bg-white border-[1px] border-gray-300 p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
            'id':'category',
        }),
        choices=CATEGORY_CHOICE,
    )

    price = forms.IntegerField(
        label = '가격',
        widget=forms.NumberInput(attrs={
            'class': 'bg-white border-[1px] border-gray-300 p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
            'id':'price',
        }),
    )

    photo = forms.ImageField(
        label='상품 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-80 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'id': 'photo',
            }
        )
    )

    tags = forms.CharField(
        label='태그',
        widget=TagWidget(
            attrs={
                'class': 'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'placeholder': '태그는 콤마(,)로 구분하여 작성해주세요',
            }
        )
    )
    
    content = forms.CharField(label='상품설명', widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = ('title', 'content', 'category', 'price', 'photo', 'tags')


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '리뷰제목',
                'placeholder': '제목을 입력해주세요',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class':'w-full bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '소개글',
                'placeholder': '리뷰를 입력해주세요',
            }
        ),
    )
    image = forms.ImageField(
        label = '사진',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-full bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
            }
        ),
        required=False
    )
    
    class Meta:
        model = Review
        fields = ('title', 'score', 'image', 'content',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_address', 'product_name', 'quantity', 'price')