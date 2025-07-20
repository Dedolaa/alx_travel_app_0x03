from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from listings app!")

# Create your views here.
