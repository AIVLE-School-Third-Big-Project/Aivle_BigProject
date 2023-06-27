from django import forms
from .models import fireVideo as Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']
