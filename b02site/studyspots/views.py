from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'studyspots/index.html')

def map(request):
    return render(request, 'studyspots/map.html')

def login(request):
    return render(request, 'studyspots/login.html')