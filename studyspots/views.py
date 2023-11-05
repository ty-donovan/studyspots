from collections import OrderedDict

from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import geopy.distance
from rest_framework.utils.serializer_helpers import ReturnList

from .forms import *

from django.urls import reverse

from studyspots.models import *


def is_ajax(request):
    return 'HTTP_X_REQUESTED_WITH' in request.META and request.META['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"


def get_studyspace_by_ordinal(location_id, location_ordinal):
    obj = StudySpace.objects.filter(location_id=location_id, location_ordinal=location_ordinal)
    if obj:
        return obj.get()
    else:
        return None


def get_variable(request, name):
    return request.GET.get(name, None)


@login_required
def profile(request):
    return redirect(reverse('studyspots:map'), False)


def confirmation(request):
    return render(request, 'studyspots/confirmation.html')


def map(request):
    starting_location_id = request.GET.get('location', None)
    key = settings.GOOGLE_API_KEY
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    context = {
        'key': key, 'locations': locations_json, 'starting_location_id': starting_location_id
    }
    return render(request, 'studyspots/map.html', context)


def map_redirect(request):
    location_id = get_variable(request, 'location')
    if location_id:
        return redirect(reverse("studyspots:map") + "?location=" + location_id, permanent=True)
    return redirect(reverse("studyspots:map"), permanent=True)


@login_required()
def add(request):
    new_location_form, new_studyspace_form = None, None
    locations = LocationSerializer(Location.objects.all(), many=True).data
    new_location_label = "-- Add new location --"
    locations_json = json.dumps(locations)
    key = settings.GOOGLE_API_KEY
    error_message = None
    # new_studyspace_form.location_form.initial = Location.objects.get(location_id=location_id)
    if request.method == 'POST':
        print(request.POST)
        selected_location = request.POST['existing_location']
        print(selected_location)
        pending_location_id = None
        if selected_location:
            location_id = int(selected_location)
        else:
            location_id = -1
        if location_id == -1:
            new_location_form = NewLocationForm(request.POST, prefix="new_location")
            if new_location_form.is_valid():
                # Get the coordinates from the form
                lat = new_location_form.cleaned_data['lat']
                lng = new_location_form.cleaned_data['lng']

                # Check if the location is within a 10-mile radius of the University of Virginia
                location_point = (lat, lng)
                uva_point = (38.0356, -78.5034)  # UVA coordinates
                distance = geopy.distance.distance(uva_point, location_point).miles

                if distance <= 10:
                    # Location is within the 10-mile radius, proceed to save
                    pending_location = PendingLocation(
                        name=new_location_form.cleaned_data['locationName'],
                        location_type=new_location_form.cleaned_data['location_type'],
                        on_grounds=new_location_form.cleaned_data['on_grounds'],
                        lat=lat,
                        lng=lng,
                    )
                    pending_location.save()
                    pending_location_id = pending_location.location_id
                else:
                    # Location is outside the 10-mile radius
                    error_message = "Location must be closer to the University of Virginia."
            else:
                error_message = "Invalid form data: you must move the pin from its original position"
        new_studyspace_form = NewStudySpaceForm(request.POST, prefix="new_studyspace")
        if new_studyspace_form.is_valid() and new_studyspace_form.cleaned_data['capacity'] > 0:
            if pending_location_id:
                pending_location = PendingLocation.objects.get(pk=pending_location_id)
            else:
                pending_location = Location.objects.get(pk=location_id)
            pending_space = PendingStudySpace(
                content_type=ContentType.objects.get_for_model(pending_location),
                object_id=pending_location.pk,
                name=new_studyspace_form.cleaned_data['studySpaceName'],
                capacity=new_studyspace_form.cleaned_data['capacity'],
                comments=[new_studyspace_form.cleaned_data['comment']],
                overall_ratings=[new_studyspace_form.cleaned_data['overall_rating']],
                comfort_ratings=[new_studyspace_form.cleaned_data['comfort_rating']],
                noise_level_ratings=[new_studyspace_form.cleaned_data['noise_level_rating']],
                crowdedness_ratings=[new_studyspace_form.cleaned_data['crowdedness_rating']],
            )
            pending_space.save()
            return redirect(reverse("studyspots:confirmation"))
        else:
            if new_studyspace_form.cleaned_data['capacity'] < 1:
                error_message = "Invalid capacity number"
                new_studyspace_form.cleaned_data['capacity'] = 1
            else:
                error_message = "Invalid study spot data"
            context = {
                'starting_location': location_id,
                'locations': locations_json,
                'make_new_location_label': new_location_label,
                'key': key,
                'new_studyspace_form': new_studyspace_form,
                'error_message': error_message,
            }
            return render(request, 'studyspots/add.html', context)
    else:
        new_location_form = NewLocationForm(prefix="new_location")
        new_studyspace_form = NewStudySpaceForm(prefix="new_studyspace")
        location_id = request.GET.get('location', None)
    context = {
        'starting_location': location_id,
        'locations': locations_json,
        'make_new_location_label': new_location_label,
        'key': key,
        'new_location_form': new_location_form,
        'new_studyspace_form': new_studyspace_form,
        'error_message': error_message,
    }
    return render(request, 'studyspots/add.html', context)


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


def get_spot(request):
    location_id = get_variable(request, 'location')
    location_ordinal = get_variable(request, 'space')
    if location_id:
        if location_ordinal:
            studyspace_obj = get_studyspace_by_ordinal(location_id, location_ordinal)
            if not studyspace_obj:
                raise Http404()
            if is_ajax(request):
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
        else:
            if is_ajax(request):
                location = Location.objects.get(location_id=location_id)
                location_data = StudySpaceSerializer(location.studyspace_set.all(), many=True).data
                return JsonResponse(location_data, safe=False)
            else:
                return redirect(reverse("studyspots:map")+"?location="+location_id)
    else:
        raise Http404()


# method to render a form to add a review for a study spot
def review_studyspace(request):
    location_id = get_variable(request, 'location')
    location_ordinal = get_variable(request, 'space')
    if location_id and location_ordinal:
        studyspace_obj = get_studyspace_by_ordinal(location_id, location_ordinal)
        return render(request, 'studyspots/studyspace_form.html',
                      {'location_id': location_id, 'studyspace': studyspace_obj})
    raise Http404()


# method to process a review for a study spot and update database
def process_studyspace_review(request):
    location_id = get_variable(request, 'location')
    location_ordinal = get_variable(request, 'space')
    if location_id and location_ordinal:
        if request.method == 'POST':
            studyspace = get_studyspace_by_ordinal(location_id, location_ordinal)
            studyspace.overall_ratings.append(int(request.POST['overall']))
            studyspace.comfort_ratings.append(int(request.POST['comfort']))
            studyspace.noise_level_ratings.append(int(request.POST['noise_level']))
            studyspace.crowdedness_ratings.append(int(request.POST['crowdedness']))
            if request.POST['comment'] != "":
                studyspace.comments.append(request.POST['comment'])
            studyspace.save()
        return redirect(reverse('studyspots:get_spot') + f'?location={location_id}&space={location_ordinal}')
    else:
        raise Http404()


def review_pending(request):
    pending_locations = PendingLocationSerializer(PendingLocation.objects.all(), many=True).data
    pending_studyspaces = PendingStudySpaceSerializer(PendingStudySpace.objects.all(), many=True).data
    return JsonResponse({"pending_locations": pending_locations, "pending_studyspaces": pending_studyspaces},
                        safe=False)
