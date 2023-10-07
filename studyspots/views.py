from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    if request.user.is_staff:
        return render(request, 'studyspots/welcome/admin.html', {'username': request.user.username})
    else:
        return render(request, 'studyspots/welcome/user.html', {'username': request.user.username})


def index(request):
    return render(request, 'studyspots/index.html')



def map(request):
    return render(request, 'studyspots/map.html')