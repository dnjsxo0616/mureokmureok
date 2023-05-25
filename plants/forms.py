from django import forms
from .models import Plant, PlantImage


class PlantImageForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class PlantForm(forms.ModelForm):
    PREFERENCES_CHOICES = [
    ('좋음', '좋음'),
    ('보통', '보통'),
    ('별로', '별로'),
    ]

    preferences = forms.MultipleChoiceField(
        label = '선호도',
        widget = forms.CheckboxSelectMultiple(attrs={
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
        ('10일', '10일'), ('15일', '15일'), ('20일', '20일'), ('없음', '없음'),
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
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices= CATEGORY_CHOICE,
    )

    WATERING_CHOICE = [
        ('주1~2회', '주1~2회'), ('월1회이하', '월1회이하'), ('월1~2회', '월1~2회'),
    ]

    watering = forms.MultipleChoiceField(
        label = '물 주기',
        widget= forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=WATERING_CHOICE,
    )

    SUNLIGHT_CHOICE = [
        ('양지', '양지'), ('음지', '음지'), ('반양지', '반양지'), ('반음지', '반음지'),
    ]

    sunlight = forms.MultipleChoiceField(
        label = '일조량',
        widget= forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=SUNLIGHT_CHOICE,
    )

    HUMIDITY_CHOICE = [
        ('40% 이하', '40% 이하'), ('40~70%', '40~70%'), ('70~90%', '70~90%'),
    ]

    humidity = forms.MultipleChoiceField(
        label = '습도',
        widget= forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices=HUMIDITY_CHOICE,
    )

    TEMPERATURE_CHOICE = [
        ('18~28도', '18~28도'), ('16~27도', '16~27도'), ('21~25도', '21~25도'),
    ]

    temperature = forms.MultipleChoiceField(
        label = '온도',
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices= TEMPERATURE_CHOICE,
    )

    BIRTHFLOWER_CHOICE = [
        ('1월', '1월'), ('2월', '2월'), ('3월', '3월'), ('4월', '4월'), ('5월', '5월'), ('6월', '6월'), ('7월', '7월'), ('8월', '8월'), ('9월', '9월'), ('10월', '10월'), ('11월', '11월'), ('12월', '12월'), ('없음', '없음'),  
    ]

    birthflower = forms.MultipleChoiceField(
        label = '탄생화',
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'id': 'category',
            'placeholder': '분류',
        }),
        choices= BIRTHFLOWER_CHOICE,
    )

    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Plant
        fields = ('title', 'content', 'preferences', 'allergy', 'flowering', 'season', 'category', 'watering', 'sunlight', 'humidity', 'temperature', 'meaning', 'birthflower', 'images',)