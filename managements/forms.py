from django import forms
from .models import Management, CalenderEntry
from django.forms.widgets import NumberInput
from plants.models import Plant

class ManagementForm(forms.ModelForm):
    plant = forms.ModelChoiceField(
        queryset=Plant.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-96 h-auto focus:outline-none focus:ring-1 focus:ring-[#1EB564]'
            }
        ),
        label='식물 선택',
        required=True
    )
    nickname = forms.CharField(
        label='식물 애칭',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '식물 애칭',
                'placeholder': '식물 애칭을 입력해주세요.',
            }
        )
    )
    managementdate = forms.DateTimeField(
        label="식물 만난 날짜",
        widget=NumberInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-auto focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'type': 'date',
            },
        ),
    )
    photo = forms.FileField(
        label = '이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-96 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'multiple': True
            }
        )
    )
    class Meta:
        model = Management
        fields = ('plant', 'photo', 'managementdate')



class CalenderEntryForm(forms.ModelForm):
    
    watering_choices = [
        ('yes', '물 줬어요!'),
        ('no', '물 안줬어요!'),
    ]
    watering = forms.ChoiceField(
        label='물주기',
        widget=forms.RadioSelect(
            attrs={
                'id': 'watering',
            }
        ),
        choices = watering_choices,
    )


    sunlight_choices = [
        ('yes', '햇빛 줬어요!'),
        ('no', '햇빛 안줬어요!'),
    ]
    sunlight = forms.ChoiceField(
        label='햇빛주기',
        widget=forms.RadioSelect(
            attrs={
                'id': 'sunlight',
            }
        ),
        choices = sunlight_choices,
    )

    humidity_choices = [
        ('40%이하', '40%이하'), ('40~70%', '40~70%'), ('70~90%', '70~90%'),
    ]
    humidity = forms.MultipleChoiceField(
        label='현재 습도',
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'id': 'humidity',
            }
        ),
        choices = humidity_choices,
    )

    TEMPERATURE_CHOICE = [
        ('18~28도', '18~28도'), ('16~27도', '16~27도'), ('21~25도', '21~25도'),
    ]

    temperature = forms.MultipleChoiceField(
        label = '온도',
        widget = forms.CheckboxSelectMultiple(attrs={
            'id': 'temperature',
        }),
        choices= TEMPERATURE_CHOICE,
    )
    things_choices = [
        ('yes', '영양제 or 비료 줬어요!'),
        ('no', '영양제 or 비료 안줬어요!'),
    ]
    things = forms.ChoiceField(
        label='영양제 or 비료 주기',
        widget=forms.RadioSelect(
            attrs={
                'id': 'things',
            }
        ),
        choices = things_choices,
    )
    significant = forms.CharField(
        label='특이 사항',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '특이 사항',
                'placeholder': '특이 사항을 입력해주세요',
            }
        )
    )
    entrydate = forms.DateTimeField(
        label="날짜",
        widget=NumberInput(
            attrs={
                'class': 'border rounded-md p-2 ps-3 w-full h-8 focus:outline-none focus:ring-1 focus:ring-[#1EB564]',
                'type': 'date',
            },
        ),
    )

    class Meta:
        model = CalenderEntry
        fields = ('watering', 'sunlight', 'humidity', 'temperature', 'things', 'significant', 'entrydate')