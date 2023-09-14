from django import forms
from .models import Community, Community_comment
from ckeditor.widgets import CKEditorWidget


class CommunityForm(forms.ModelForm):
    content = forms.CharField(label='게시글 내용', widget=CKEditorWidget())

    class Meta:
        model = Community
        fields = ('title', 'content', 'photo', 'need_expert', 'category')

    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '게시글 제목',
                'placeholder': '게시글 제목을 입력해주세요',
            }
        )
    )

    photo = forms.ImageField(
        label='썸네일 사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-80 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'id': 'photo',
            }
        )
    )

    need_expert = forms.BooleanField(
        label='전문가 답변 필요 여부',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'w-4 h-4 bg-[#1EB564]',
                'id': 'need_expert',
            }
        )
        ,required=False,
    )
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'bg-white border-[1px] border-gray-300 p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
            }
        ),
        choices = (('실내 식물','실내 식물'), ('실외 식물', '실외 식물'),
                    ('실내 식물 종자', '실내 식물 종자'), ('실외 식물 종자', '실외 식물 종자'), ('전문가 Q&A','전문가 Q&A'), ('운영자 Q&A', '운영자 Q&A'),
        ), 
        required=True,
    )


class Community_commentForm(forms.ModelForm):
    class Meta:
        model = Community_comment
        fields = ('content',)

    content = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'class' : 'w-full py-2 bg-transparent border-0 border-gray-300 border-b-[1px] focus:outline-none focus:border-b-[#1EB564]',
                'placeholder' : '댓글을 작성해주세요',
            }
        )
    )