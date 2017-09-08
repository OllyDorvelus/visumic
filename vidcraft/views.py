__author__ = 'OllyD'

from django.shortcuts import render
from django.forms import model_to_dict
from django.http import JsonResponse
from videos.models import PlaylistModel


def home(request):

    return render(request, "index.html", {})

def about(request):
    return render(request, "about.html", {})

def policy(request):
    return render(request, "policy.html", {})

def help(request):
    return render(request, "help.html", {})


def live_unread_notification_list(request):
    if not request.user.is_authenticated():
        data = {
           'unread_count':0,
           'unread_list':[]
        }
        return JsonResponse(data)

    try:
        num_to_fetch = request.GET.get('max', 5)  # If they don't specify, make it 5.
        num_to_fetch = int(num_to_fetch)
        num_to_fetch = max(1, num_to_fetch)  # if num_to_fetch is negative, force at least one fetched notifications
        num_to_fetch = min(num_to_fetch, 100)  # put a sane ceiling on the number retrievable
    except ValueError:
        num_to_fetch = 5  # If casting to an int fails, just make it 5.

    unread_list = []

    for n in request.user.notifications.all()[0:num_to_fetch]:
        struct = model_to_dict(n)
        if n.actor:
            struct['actor'] = str(n.actor)
        if n.target:
            struct['target'] = str(n.target)
        if n.action_object:
            struct['action_object'] = str(n.action_object)
        unread_list.append(struct)
        if request.GET.get('mark_as_read'):
            n.mark_as_read()
    data = {
        'unread_count': request.user.notifications.unread().count(),
        'unread_list': unread_list
    }
    return JsonResponse(data)