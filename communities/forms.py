from django import forms
from .models import Community, Community_comment



class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('title', 'content', 'photo', 'need_expert',)

    title = forms.CharField(
        label='게시글 제목',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': '게시글 제목',
                'placeholder': '게시글 제목을 입력해주세요',
            }
        )
    )

    content = forms.CharField(
        label='게시글 내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id' : 'content',
            }
        )
    )

    photo = forms.ImageField(
        label='사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-contol',
                'id': 'photo',
            }
        )
    )

    need_expert = forms.BooleanField(
        label='전문가 답변 필요 여부',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'need_expert',
            }
        )
        ,required=False,
    )


class Community_commentForm(forms.ModelForm):
    class Meta:
        model = Community_comment
        fields = ('content',)

    content = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'class' : 'form-control',
                'placeholder' : '댓글을 입력해주세요!'
            }
        )
    )