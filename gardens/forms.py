from django import forms
from .models import Garden, Comment
from ckeditor.widgets import CKEditorWidget


class GardenForm(forms.ModelForm):
    title = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '식물원 이름',
                'placeholder': '식물원 또는 축제 이름을 입력해주세요',
            }
        )
    )
    content = forms.CharField(label='세부정보', widget=CKEditorWidget())
    ex_content = forms.CharField(
        label='소개글',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '소개글',
                'placeholder': '소개글을 입력해주세요',
            }
        )
    )
    # latitude = forms.FloatField(label='위도')
    # longitude = forms.FloatField(label='경도')
    address = forms.CharField(
        label='위치',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '주소',
                'placeholder': '주소를 입력해주세요',
            }
        )
    )  # 주소 필드 추가
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'bg-white border-[1px] border-gray-300 p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
            }
        ),
        choices = (('식물원','식물원'), ('전시회', '전시회'),
                    ('정원센터', '정원센터'), ('축제', '축제'),
                    ), 
        required=True,
    )
    image = forms.ImageField(
        label='썸네일 사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-80 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'id': 'photo',
            }
        ),
    )
    site_link = forms.URLField(
        label='관련 사이트 링크',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '사이트 링크',
                'placeholder': '링크를 입력해주세요',
            }
        ),
        required=False,
    )
    query = forms.CharField(
        label='검색어',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '검색어',
                'placeholder': '검색어를 입력해주세요',
            }
        ),
    )
    class Meta:
        model = Garden
        fields = ('title', 'content', 'ex_content', 'address', 'category', 'image', 'site_link',)


class CommentForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '후기제목',
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
                'placeholder': '후기를 입력해주세요',
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
        model = Comment
        fields = ('title', 'score', 'content', 'image',)
