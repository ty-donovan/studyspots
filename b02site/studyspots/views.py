from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'studyspots/index.html')

def map(request):
    return render(request, 'studyspots/map.html')
