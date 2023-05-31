from django import forms
from .models import Notice
from ckeditor.widgets import CKEditorWidget

class NoticeForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Notice
        fields = ('title', 'content', 'thumbnail',)

    title = forms.CharField(
        label='게시글 제목',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control w-75',
                'id': '게시글 제목',
                'placeholder': '게시글 제목을 입력해주세요',
            }
        )
    )


    thumbnail = forms.ImageField(
        label='사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-contol w-75',
                'id': 'Thumbnail',
            }
        )
    )


