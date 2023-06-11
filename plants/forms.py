from django import forms
from .models import Plant, PlantImage
from taggit.forms import TagField, TagWidget


class PlantImageForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class PlantForm(forms.ModelForm):
    title = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                'class':'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
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

    # Allergy_CHOICES = [
    #     ('알러지1', '알러지1'), ('알러지2', '알러지2'),
    # ]

    # allergy = forms.MultipleChoiceField(
    #     label = '알레르기',
    #     widget = forms.CheckboxSelectMultiple(attrs={
    #         'class': 'form-control',
    #         'id': 'category',
    #         'placeholder': '분류',
    #     }),
    #     choices = Allergy_CHOICES,
    # )

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

    # FLOWERING_CHOICE = [
    #     ('10일', '10일'), ('15일', '15일'), ('20일', '20일'), ('없음', '없음'),
    # ]

    # flowering = forms.MultipleChoiceField(
    #     label = '개화시기',
    #     widget = forms.CheckboxSelectMultiple(attrs={
    #         'class': 'form-control',
    #         'id': 'category',
    #         'placeholder': '분류',
    #     }),
    #     choices = FLOWERING_CHOICE,
    # )

    # FLOWERING_CHOICE = [(str(i), str(i)) for i in range(1, 31)]

    # flowering = forms.ChoiceField(
    #     label='개화시기',
    #     widget=forms.Select(attrs={
    #         'class': 'bg-white border-[1px] border-gray-300 p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
    #         'id': 'blossom',
    #     }),
    #     choices=FLOWERING_CHOICE,
    # )

    # SEASON_CHOICE = [
    #     ('사계절', '사계절'), ('봄', '봄'), ('여름', '여름'), ('가을', '가을'), ('겨울', '겨울'),
    # ]

    # season = forms.MultipleChoiceField(
    #     label = '계절',
    #     widget = forms.CheckboxSelectMultiple(attrs={
    #         'id': 'season',
    #     }),
    #     choices = SEASON_CHOICE,
    # )

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
        ('주 1~2회', '주 1~2회'), ('주 2~3회', '주 2~3회'), ('주 3~4회', '주 3~4회'),
        ('주 4~5회', '주 4~5회'), ('월1~2회', '월1~2회'), ('월1회이하', '월1회이하')
    ]

    watering = forms.MultipleChoiceField(
        label = '물 주기',
        widget= forms.CheckboxSelectMultiple(attrs={
            'id': 'watering',
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
                'class': 'w-96 bg-white border rounded-md focus:outline-none focus:ring-1 focus:ring-[#1EB564] text-gray-400',
                'multiple': True
            }
        )
    )

    tags = forms.CharField(
        label='태그',
        widget=TagWidget(
            attrs={
                'class': 'w-96 bg-white border-[1px] p-1 px-2 rounded-lg focus:outline-none focus:border-[#1EB564] focus:border-[2px]',
                'placeholder': '태그는 콤마(,)로 구분하여 작성해주세요',
            }
        )
    )
    class Meta:
        model = Plant
        fields = ('title', 'content', 'allergy', 'category', 'watering', 'sunlight', 'humidity', 'temperature',  'images', 'tags',)