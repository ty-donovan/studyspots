from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
import json
from studyspots.models import *


def is_ajax(request):
    return 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"


@login_required
def profile(request):
    if request.user.is_staff:
        return render(request, 'studyspots/welcome/admin.html', {'username': request.user.username})
    else:
        return render(request, 'studyspots/welcome/user.html', {'username': request.user.username})


#
# @login_required
# def welcome_admin(request):
#     if request.user.user_role == 'admin':
#         return render(request, 'studyspots/welcome/admin.html', {'username': request.user.username})
#     else:
#         return render(request, 'studyspots/welcome/user.html', {'username': request.user.username})
#
#
# @login_required
# def welcome_user(request):
#     if request.user.user_role == 'user':
#         return render(request, 'studyspots/welcome/user.html', {'username': request.user.username})
#     else:
#         return render(request, 'studyspots/welcome/admin.html', {'username': request.user.username})
#


def index(request):
    return render(request, 'studyspots/index.html')


def map(request):
    key = settings.GOOGLE_API_KEY
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    context = {
        'key': key, 'locations': locations_json
    }
    # return JsonResponse(list(locations), safe=False)
    return render(request, 'studyspots/map.html', context)


def add(request, location_id=None):
    if location_id is not None:
        print("a")
    return render(request, 'studyspots/add.html')


# Add all the locations from the file to database. Do not use.
def load(request):
    json_response = dict({"Success": "Resource successfully added to database"})
    if Location.objects.exists():
        json_response = {"No need": "Locations db already populated"}
    else:
        with open('locations.json') as json_file:
            locations = json.load(json_file)
        for location_dict in locations:
            location = Location()
            for k, v in location_dict.items():
                setattr(location, k, v)
            location.save()
    return JsonResponse(json_response, safe=False)


def get_location_data(request, location_id):
    if request.method == "GET" and is_ajax(request):
        location = Location.objects.get(location_id=location_id)
        location_data = StudySpaceSerializer(location.studyspace_set.all(), many=True).data
        return JsonResponse(location_data, safe=False)
    # render(request, )


def get_studyspace_data(request, location_id, studyspace_id):
    if request.method == "GET" and is_ajax(request):
        location = Location.objects.get(location_id=location_id)
        studyspace_data = StudySpaceSerializer(location.studyspace_set.get(studyspace_id=studyspace_id), many=True).data
        return JsonResponse(studyspace_data, safe=False)
