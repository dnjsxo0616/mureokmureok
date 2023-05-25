from django import forms
from .models import Garden, Comment
from ckeditor.widgets import CKEditorWidget


class GardenForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Garden
        fields = ('title', 'content', 'latitude', 'longitude', 'category', 'image', 'site_link')
        
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
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'

