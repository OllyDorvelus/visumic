from django.shortcuts import render
from django.views import View

# Create your views here.

from .models import HashTagModel



class HashTagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = HashTagModel.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_view.html', {"hashtag": obj})