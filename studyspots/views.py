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

def confirmation(request):
    return render(request, 'studyspots/confirmation.html')


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
                return redirect('studyspots:addNewSpot', location_id=location_id)

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
            error_message = "Invalid form data: you must move the pin from it's original position"
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
