from django import forms
from .models import Plant, PlantImage
from taggit.forms import TagField, TagWidget


class PlantImageForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(),
        }

class PlantForm(forms.ModelForm):
    title = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                'class':'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': 'title',
                'placeholder': '식물 이름을 입력해주세요',
            }
        )
    )
    content = forms.CharField(
        label='설명',
        widget=forms.Textarea(
            attrs={
                'class':'w-full h-60 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': '설명글',
                'placeholder': '설명글을 입력해주세요',
            }
        ),
    )


    Allergy_CHOICES = [
        ('yes', '꽃가루 알러지 있음'),
        ('no', '꽃가루 알러지 없음'),
    ]

    allergy = forms.ChoiceField(
        label='알레르기',
        widget=forms.RadioSelect(
            attrs={
                'id': 'allergy',
            }
        ),
        choices=Allergy_CHOICES,
    )


    CATEGORY_CHOICE = [
        ('실내식물', '실내식물'), ('실외식물', '실외식물'),
    ]

    category = forms.MultipleChoiceField(
        label = '카테고리',
        widget = forms.CheckboxSelectMultiple(attrs={
            'id': 'category',
        }),
        choices= CATEGORY_CHOICE,
    )

    WATERING_CHOICE = [
        ('주1~2회', '주1~2회'), ('주2~3회', '주2~3회'), ('주3~4회', '주3~4회'),
        ('주4~5회', '주4~5회'), ('월1~2회', '월1~2회'), ('월1회이하', '월1회이하')
    ]

    watering = forms.MultipleChoiceField(
        label = '물 주기',
        widget= forms.CheckboxSelectMultiple(attrs={
            'id': 'watering',
            'class': 'w-full flex-wrap',
        }),
        choices=WATERING_CHOICE,
    )

    SUNLIGHT_CHOICE = [
        ('양지', '양지'), ('반양지', '반양지'), ('반음지', '반음지'), ('음지', '음지'),
    ]

    sunlight = forms.MultipleChoiceField(
        label = '일조량',
        widget= forms.CheckboxSelectMultiple(attrs={
            'id': 'sunlight',
            'class': 'w-full flex-wrap flex gap-5 sm:gap-0',
        }),
        choices=SUNLIGHT_CHOICE,
    )

    HUMIDITY_CHOICE = [
        ('40%이하', '40%이하'), ('40~70%', '40~70%'), ('70~90%', '70~90%'),
    ]

    humidity = forms.MultipleChoiceField(
        label = '습도',
        widget= forms.CheckboxSelectMultiple(attrs={
            'id': 'humidity',
        }),
        choices=HUMIDITY_CHOICE,
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

    images = forms.FileField(
        label = '이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'w-80 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
            }
        )
    )

    tags = forms.CharField(
        label='태그',
        widget=TagWidget(
            attrs={
                'class': 'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'placeholder': '태그는 콤마(,)로 구분하여 작성해주세요',
            }
        )
    )

    price = forms.IntegerField(  # 가격 필드 추가
        label='가격',
        widget=forms.NumberInput(
            attrs={
                'class': 'w-80 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'id': 'price',
                'placeholder': '가격을 입력해주세요',
            }
        ),
    )
    class Meta:
        model = Plant
        fields = ('title', 'content', 'allergy', 'category', 'watering', 'sunlight', 'humidity', 'temperature', 'price','images', 'tags',)