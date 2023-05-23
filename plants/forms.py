from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    PREFERENCES_CHOICES = [
    ('좋음', '좋음'),
    ('보통', '보통'),
    ('별로', '별로'),
    ]

    preferences = forms.MultipleChoiceField(
        label = '선호도',
        widget = forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices = PREFERENCES_CHOICES,
    )

    Allergy_CHOICES = [
        ('알러지1', '알러지1'), ('알러지2', '알러지2'),
    ]

    allergy = forms.MultipleChoiceField(
        label = '알레르기',
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices = Allergy_CHOICES,
    )

    FLOWERING_CHOICE = [
        ('10일', '10일'), ('15일', '15일'), ('20일', '20일'),
    ]

    flowering = forms.MultipleChoiceField(
        label = '개화시기',
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices = FLOWERING_CHOICE,
    )


    SEASON_CHOICE = [
        ('겨울', '겨울'), ('봄', '봄'), ('여름', '여름'), ('가을', '가을'),
    ]

    season = forms.MultipleChoiceField(
        label = '계절',
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices = SEASON_CHOICE,
    )


    CATEGORY_CHOICE = [
        ('실내식물', '실내식물'), ('실외식물', '실외식물'),
    ]

    category = forms.MultipleChoiceField(
        label = '카테고리',
        widget = forms.CheckboxInput(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices= CATEGORY_CHOICE,
    )

    WATERING_CHOICE = [
        ('주1회', '주1회'), ('주2회', '주2회'), ('주3회', '주3회'),
    ]

    watering = forms.MultipleChoiceField(
        label = '물 주기',
        widget= forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=WATERING_CHOICE,
    )

    SUNLIGHT_CHOICE = [
        ('양지', '양지'), ('음지', '음지'), ('반양지', '반양지'), ('반음지', '반음지'),
    ]

    watering = forms.MultipleChoiceField(
        label = '일조량',
        widget= forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=SUNLIGHT_CHOICE,
    )

    HUMIDITY_CHOICE = [
        ('10~30%', '10~30%'), ('40~70%', '40~70%'), ('70~90%', '70~90%'),
    ]

    humidity = forms.MultipleChoiceField(
        label = '습도',
        widget= forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=HUMIDITY_CHOICE,
    )

    TEMPERATURE_CHOICE = [
        ('0 ~ 10도', '0 ~ 10도'), ('10 ~ 20도', '10 ~ 20도'), ('20 ~ 30도', '20 ~ 30도'),
    ]

    Temperature = forms.MultipleChoiceField(
        label = '온도',
        widget = forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices= TEMPERATURE_CHOICE,
    )

    class Meta:
        model = Plant
        fields = '__all__'