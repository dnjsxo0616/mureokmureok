from django import forms
from .models import Garden, Comment
from ckeditor.widgets import CKEditorWidget


class GardenForm(forms.ModelForm):
    content = forms.CharField(label='내용', widget=CKEditorWidget())
    title = forms.CharField(label='제목')
    ex_content = forms.CharField(label='추가 내용')
    # latitude = forms.FloatField(label='위도')
    # longitude = forms.FloatField(label='경도')
    address = forms.CharField(label='주소')  # 주소 필드 추가
    # category = forms.CharField(label='카테고리')
    image = forms.ImageField(label='이미지')
    site_link = forms.URLField(label='사이트 링크')

    class Meta:
        model = Garden
        fields = ('title', 'content', 'ex_content', 'address', 'category', 'image', 'site_link')
        labels = {
            'title': '제목',
            'content': '내용',
            'ex_content': '추가 내용',
            'address': '주소',  # 주소 필드 레이블 추가
            'category': '카테고리',
            'image': '이미지',
            'site_link': '사이트 링크',
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='내용')
    image = forms.ImageField(
        label = False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    class Meta:
        model = Comment
        fields = ('content','image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'

