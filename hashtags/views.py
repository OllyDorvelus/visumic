from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

# Create your views here.

from .models import HashTagModel



class HashTagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        obj, created = HashTagModel.objects.get_or_create(tag=hashtag)
        return render(request, 'hashtags/tag_view.html', {"hashtag": obj})

class HashTagList(ListView):
    template_name = 'hashtags/hashtag_list.html'
    context_object_name = 'all_hashtags'
    # paginate_by = 10

    def get_queryset(self):
        #add.delay(3,2)
        return HashTagModel.objects.all()