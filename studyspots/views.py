from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import serializers
import json
import geopy.distance
from .forms import newLocationForm
from .forms import existingLocationForm
from .models import Location
from .forms import SelectExistingLocationForm
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

def confirmation(request):
    return render(request, 'studyspots/confirmation.html')


def map(request):
    key = settings.GOOGLE_API_KEY
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    context = {
        'key': key, 'locations': locations_json
    }
    # return JsonResponse(list(locations), safe=False)
    return render(request, 'studyspots/map.html', context)

# def add(request):
#     return render(request, 'studyspots/add.html')
def add(request):
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    if request.method == 'POST':
        existing_location_form = SelectExistingLocationForm(request.POST)

        if existing_location_form.is_valid():
            selected_location = existing_location_form.cleaned_data['existing_location']
            
            # Redirect to the "addSpot" URL with the selected location's ID
            if selected_location:
                location_id = selected_location.location_id
                return redirect('addSpot', location_id=location_id)
    
    else:
        existing_location_form = SelectExistingLocationForm()
    context = {
        'locations': locations_json,
        'existing_location_form': existing_location_form,
    }
    return render(request, 'studyspots/add.html', context)

def nonExistingLocation(request):
    key = settings.GOOGLE_API_KEY
    error_message = None

    if request.method == 'POST':
        form = newLocationForm(request.POST)
        if form.is_valid():
            # Get the coordinates from the form
            lat = form.cleaned_data['lat']
            lng = form.cleaned_data['lng']

            # Check if the location is within a 10-mile radius of the University of Virginia
            location_point = (lat, lng)
            uva_point = (38.0356, -78.5034) # UVA coordinates
            distance = geopy.distance.distance(uva_point, location_point).miles

            if distance <= 10:
                # Location is within the 10-mile radius, proceed to save
                location = PendingLocation(
                    name=form.cleaned_data['locationName'],
                    location_type=form.cleaned_data['location_type'],
                    on_grounds=form.cleaned_data['on_grounds'],
                    lat=lat,
                    lng=lng,
                )
                location.save()

                spot = PendingStudySpot(
                    content_type=ContentType.objects.get_for_model(location),
                    object_id=location.pk,
                    name=form.cleaned_data['spotName'],
                    capacity = form.cleaned_data['capacity'],
                    comments=[form.cleaned_data['comment']],
                    overall_ratings=[form.cleaned_data['overall_rating']],
                    comfort_ratings=[form.cleaned_data['comfort_rating']],
                    noise_level_ratings=[form.cleaned_data['noise_level_rating']],
                    crowdedness_ratings=[form.cleaned_data['crowdedness_rating']],
                )
                spot.save()

                # Redirect to map page or any other desired action
                return redirect("../../confirmation")
            else:
                # Location is outside the 10-mile radius
                error_message = "Location must be closer to the University of Virginia."
        else:
            error_message = "Invalid form data. Note: You must move the pin from it's original position"
    else:
        form = newLocationForm()

    context = {
        'key': key,
        'form': form,
        'error_message': error_message,
    }

    return render(request, 'studyspots/addNewLocation.html', context)

def addNewSpot(request, location_id):
    error_message = None

    if request.method == 'POST':
        form = existingLocationForm(request.POST)
        if form.is_valid():
            location = Location.objects.get(pk=location_id)
            spot = PendingStudySpot(
                    content_type=ContentType.objects.get_for_model(location),
                    object_id=location.pk,
                    name=form.cleaned_data['spotName'],
                    capacity = form.cleaned_data['capacity'],
                    comments=[form.cleaned_data['comment']],
                    overall_ratings=[form.cleaned_data['overall_rating']],
                    comfort_ratings=[form.cleaned_data['comfort_rating']],
                    noise_level_ratings=[form.cleaned_data['noise_level_rating']],
                    crowdedness_ratings=[form.cleaned_data['crowdedness_rating']],
            )
            spot.save()

                # Redirect to map page or any other desired action
            return redirect("../../confirmation")
        else:
            error_message = "Invalid form data."
    else:
        form = existingLocationForm()

    context = {
        'form': form,
        'error_message': error_message,
    }
    
    return render(request, 'studyspots/addNewSpot.html', context)


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



    
