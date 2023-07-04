from django import forms
from .models import fireVideo as Video
from django.shortcuts import render

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

def your_view(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # 필요한 로직 수행
            return redirect('/')  # 리다이렉트할 URL을 설정

    else:
        form = VideoForm()

    context = {
        'form': form
    }
    return render(request, 'your_template.html', context)