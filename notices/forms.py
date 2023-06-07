from django import forms
from .models import Notice
from ckeditor.widgets import CKEditorWidget

class NoticeForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Notice
        fields = ('title', 'content', 'thumbnail',)

    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '게시글 제목',
                'placeholder': '게시글 제목을 입력해주세요',
            }
        )
    )

    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class':'w-full h-60 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '내용',
                'placeholder': '내용을 입력해주세요',
            }
        ),
    )

    thumbnail = forms.ImageField(
        label='사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-96 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'id': 'photo',
            }
        )
    )


