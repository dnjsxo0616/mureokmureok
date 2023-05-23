from django import forms
from .models import Garden

class GardenForm(forms.ModleForm):
    class Meta:
        model = Garden
        fields = ('title','content','location_garden','category','image','site_link')