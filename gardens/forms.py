from django import forms
from .models import Garden, Comment

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ('title','content','location_garden','category','image','site_link')

        
class CommentForm(forms.ModelForm):
    image = forms.ImageField(
        label = False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    class Meta:
        model = Comment
        fields = ('content','image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['content'].widget.attrs['placeholder'] = '다른 고객님에게 도움이 되도록 상품에 대한 솔직한 평가를 남겨주세요.'
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'

