from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#from django.template.context_processors import request


def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')