from django import forms
from .models import Supply
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager
from ckeditor.widgets import CKEditorWidget


class SupplyForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Supply
        fields = ('supply_name', 'category', 'price', 'content', 'photo', 'tags',)
        widgets = {
            'tags':TagWidget(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '콤마로 구분하여 입력해주세요',
                }
            ),        
        }
        help_texts = {
            'tags': '콤마로 구분하여 입력해주세요',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = '태그'

    supply_name = forms.CharField(
        label='소모품명',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': '소모품명',
                'placeholder': '소모품명을 입력해주세요',
            }
        )
    )

    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'category',
                'placeholder': '분류',
            }
        )
    )

    price = forms.IntegerField(
        label='소모품 가격',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id': 'price',
                'step': '50',
            }
        )
    )

    photo = forms.ImageField(
        label='제품 사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'id' : 'photo',
            }
        )
    )

    # content = forms.CharField(
    #     label='제품 설명',
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'id' : 'content',
    #         }
    #     )
    # )


