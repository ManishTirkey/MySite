from django.shortcuts import render as ren
from django.http import HttpResponse as res


# Create your views here.
def index(request):
    return res("this is index")

