__author__ = 'OllyD'

from django.shortcuts import render

def home(request):
    return render(request, "index.html", {})