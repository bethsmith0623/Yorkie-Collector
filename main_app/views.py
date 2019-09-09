from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse ('Welcome to Yorkie Collector!')

def about(request):
    return HttpResponse ('This is Beth\'s Yorkie Collector!')