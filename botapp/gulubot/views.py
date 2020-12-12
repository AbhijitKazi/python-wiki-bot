from django.shortcuts import render
from . import botserver

# Create your views here.
# Index view

def index(request):
    return render(request, 'index.html', context = None)
