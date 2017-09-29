from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
#from profiles.models import Userprofile
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, DetailView, ListView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from videos.models import VideoModel
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from videos.forms import ShareEditForm
from videos.models import PlaylistModel
from accounts.tasks import add
from .models import EventModel
from .forms import EventModelForm
from videos.mixins import UserOwnerMixin
# Create your views here.

class EventDetailView(DetailView):
    model = EventModel
    template_name = "events/event_detail.html"
    context_object_name = 'event'

class EventListView(ListView):
    model = EventModel
    template_name = 'events/event_list.html'
    context_object_name = 'events'

class EventCreateView(CreateView):
    model = EventModel
    form_class = EventModelForm
    template_name = "events/event_create.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:home")
        else:
            return super(EventCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)

class EventUpdateView(UpdateView, LoginRequiredMixin, UserOwnerMixin):
    template_name = "events/event_edit.html"
    model = EventModel
    form_class = EventModelForm
    #fields = ['name', 'thumbnail', 'description', 'genre']



    def get_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        event = EventModel.objects.get(pk=pk)
        return event

    def dispatch(self, request, *args, **kwargs):
        event = EventUpdateView.get_object(self)
        if not request.user.is_authenticated:
            return redirect("accounts:home")
        if event.user != self.request.user:
            return redirect("accounts:home")
        else:
            return super(EventUpdateView, self).dispatch(request, *args, **kwargs)