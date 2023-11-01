from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
import json

from django.urls import reverse

from studyspots.models import *


def is_ajax(request):
    return 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"


def get_studyspace_by_ordinal(location_id, location_ordinal):
    return StudySpace.objects.filter(location_id=location_id, location_ordinal=location_ordinal).get()


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


# def index(request):
#     return render(request, 'studyspots/index.html')


def map(request):
    key = settings.GOOGLE_API_KEY
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    context = {
        'key': key, 'locations': locations_json
    }
    return render(request, 'studyspots/map.html', context)


def map_redirect(request):
    return redirect(reverse('studyspots:map'), False)


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


def get_studyspace_data(request, location_id, location_ordinal):
    studyspace_obj = get_studyspace_by_ordinal(location_id, location_ordinal)
    if request.method == "GET" and is_ajax(request):
        studyspace_data = StudySpaceSerializer(studyspace_obj, many=False).data
        return JsonResponse(studyspace_data, safe=False)
    else:
        # used to render information about a study spot
        rating = dict()
        rating['overall'] = studyspace_obj.calculate_overall_rating()
        rating['comfort'] = studyspace_obj.calculate_comfort_rating()
        rating['noise_level'] = studyspace_obj.calculate_noise_level_rating()
        rating['crowdedness'] = studyspace_obj.calculate_crowdedness_rating()
        return render(request, 'studyspots/studyspace.html',
                      {'studyspace': studyspace_obj, 'location_id': location_id, 'rating': rating})


# method to render a form to add a review for a study spot
def review_studyspace(request, location_id, location_ordinal):
    studyspace_obj = get_studyspace_by_ordinal(location_id, location_ordinal)
    return render(request, 'studyspots/studyspace_form.html',
                  {'location_id': location_id, 'studyspace': studyspace_obj})


# method to process a review for a study spot and update database
def process_studyspace_review(request, location_id, location_ordinal):
    if request.method == 'POST':
        studyspace = get_studyspace_by_ordinal(location_id, location_ordinal)
        studyspace.overall_ratings.append(int(request.POST['overall']))
        studyspace.comfort_ratings.append(int(request.POST['comfort']))
        studyspace.noise_level_ratings.append(int(request.POST['noise_level']))
        studyspace.crowdedness_ratings.append(int(request.POST['crowdedness']))
        if request.POST['comment'] != "":
            studyspace.comments.append(request.POST['comment'])
        studyspace.save()
        return redirect('studyspots:get_studyspace_data', location_id=location_id, location_ordinal=location_ordinal)
    else:
        return redirect('studyspots:get_studyspace_data', location_id=location_id, location_ordinal=location_ordinal)
