from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms.widgets import NumberInput

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='사용자 ID',
        widget=forms.TextInput(
            attrs={
                'class': 'bg-gray-100 rounded-lg p-2 ps-4 w-full focus:outline-none focus:ring-1 focus:ring-[#1EB564] m-0',
                'id': '사용자 ID',
                'placeholder': '아이디를 입력해주세요',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'bg-gray-100 rounded-lg p-2 ps-4 w-full focus:outline-none focus:ring-1 focus:ring-[#1EB564] m-0',
                'id': '비밀번호',
                'placeholder': '비밀번호를 입력해주세요',
            }
        )
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='사용자 ID',
        widget=forms.TextInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id': '사용자 ID',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id': '비밀번호',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id': '비밀번호 확인',
            }
        )
    )
    email = forms.CharField(
        label='이메일',
        widget=forms.EmailInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id': '이메일',
            }
        )
    )
    image = forms.ImageField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'border rounded-md w-full focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-[14px]',
            },
        ),
        required=False,
    )
    birthday = forms.DateTimeField(
        label="날짜",
        widget=NumberInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'type': 'date',
            },
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username', 'password1', 'password2', 'email','image',
        )


class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField(
        label='이메일',
        widget=forms.EmailInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id' : '이메일',
            }
        )
    )

    image = forms.ImageField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'border rounded-md w-full focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-[14px]',
                'id' : 'id_image',
            },
        ),
        required=False,
    )

    password = None
    
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email','image',)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='기존 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id' : '기존 비밀번호',
            },
        ),
    )
    new_password1= forms.CharField(
        label='새 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id' : '새 비밀번호',
            },
        ),
    )
    new_password2 = forms.CharField(
        label='새 비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'id' : '새 비밀번호 확인',
            },
        ),
    )   