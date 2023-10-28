from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
import json
from studyspots.models import *


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

def add(request):
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


def get_location_data(request):
    pass


def get_spot_data(request, location_id):
    study_spot = {"404": "Resource not found"}
    if request.method == "GET":
        location = Location.objects.get(location_id=location_id)
        study_spot = StudySpotSerializer(location.studyspot_set.all(), many=True).data
    return JsonResponse(study_spot, safe=False)


# method to render information about a study spot
def study_spot(request, location_id, study_spot_id):
    study_spot = StudySpot.objects.get(space_id=study_spot_id)
  
    return render(request, 'studyspots/study_spot.html', {'study_spot': study_spot, 'location_id': location_id})


# method to render a form to add a review for a study spot
def review_spot(request, location_id, study_spot_id):
    study_spot = StudySpot.objects.get(space_id=study_spot_id)

    return render(request, 'studyspots/study_spot_form.html', {'study_spot_id': study_spot_id,
                                                                'location_id': location_id,
                                                                'study_spot': study_spot})


# method to process a review for a study spot and update database
def process_review(request, location_id, study_spot_id):
    if request.method == 'POST':
        study_spot = StudySpot.objects.get(space_id=study_spot_id)
        study_spot.overall_ratings.append(int(request.POST['overall']))
        study_spot.comfort_ratings.append(int(request.POST['comfort']))
        study_spot.noise_level_ratings.append(int(request.POST['noise_level']))
        study_spot.crowdedness_ratings.append(int(request.POST['crowdedness']))

        if request.POST['comment'] != "":
            study_spot.comments.append(request.POST['comment'])

        study_spot.save()
        return redirect('studyspots:study_spot', location_id=location_id, study_spot_id=study_spot_id)
    else:
        return redirect('studyspots:study_spot', location_id=location_id, study_spot_id=study_spot_id)
    