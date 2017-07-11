from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from videos.models import GenreModel


# Create your views here.








class ChartView(ListView):
    template_name = "charts/chartbase.html"
    model = GenreModel
    context_object_name = 'category'

    def get_object(self):
        categories = GenreModel.objects.filter(is_category=True)
        genre = get_object_or_404(categories, genrename__iexact=self.kwargs.get("category"))
        return genre

    def get_context_data(self, *args, **kwargs):
        context = super(ChartView, self).get_context_data(*args, **kwargs)
        category = self.kwargs.get("category")
        category = GenreModel.objects.get(genrename__iexact=category)
        genres = GenreModel.objects.filter(parent_id=category.pk)
        context['Genres'] = genres
        return context

class ChartViewAllTime(DetailView):
    template_name = "charts/chartlist_alltime.html"
    model = GenreModel
    context_object_name = 'category'
    #return render(request, "charts/chartlist_alltime.html", {})
    def get_object(self):
        categories = GenreModel.objects.filter(is_category=True)
        genre = get_object_or_404(categories, genrename__iexact=self.kwargs.get("category"))
        return genre

    def get_context_data(self, *args, **kwargs):
        context = super(ChartViewAllTime, self).get_context_data(*args, **kwargs)
        category = self.kwargs.get("category")
        category = GenreModel.objects.get(genrename__iexact=category)
        genres = GenreModel.objects.filter(parent_id=category.pk)
        categories = GenreModel.objects.filter(is_category=True)
        context['categories'] = categories
        context['Genres'] = genres
        return context

# class ChartViewAllTimeGenre(DetailView):
#     model = GenreModel
#     template_name = "charts/chartlist_alltime_genre.html"
#     context_object_name = "genre"
#
#
#     def get_object(self):
#         genre = get_object_or_404(GenreModel, genrename__iexact=self.kwargs.get("genrename"))
#         return genre

def ChartViewDaily(request):
    return render(request, "charts/chartlist_daily.html", {})