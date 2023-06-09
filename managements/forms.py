from django import forms
from .models import Management, CalenderEntry
from django.forms.widgets import NumberInput

class ManagementForm(forms.ModelForm):
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
        fields = ('watering', 'sunlight', 'humidity', 'temperature', 'entrydate')