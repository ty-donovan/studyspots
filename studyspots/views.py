from collections import OrderedDict
from json import JSONDecodeError

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
    starting_location_id = request.GET.get('location', "null")
    key = settings.GOOGLE_API_KEY
    location_objs = Location.objects.all().filter(studyspace__isnull=False).distinct().order_by("name")
    space_objs = StudySpace.objects.all().order_by("location_ordinal").order_by("location_id")
    locations = LocationSerializer(Location.objects.all(), many=True).data
    locations_json = json.dumps(locations)
    context = {
        'key': key, 'locations': locations_json, 'starting_location_id': starting_location_id,
        'location_objs': location_objs, 'space_objs': space_objs
    }
    return render(request, 'studyspots/map.html', context)


def map_redirect(request):
    location_id = get_variable(request, 'location')
    if location_id:
        return redirect(reverse("studyspots:map") + "?location=" + location_id, permanent=True)
    return redirect(reverse("studyspots:map"), permanent=True)


# this is a mess rn
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
        pending_location = None
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
                        lng=lng
                    )
                else:
                    # Location is outside the 10-mile radius
                    error_message = "Location must be closer to the University of Virginia."
            else:
                error_message = "Invalid form data: you must move the pin from its original position"
        else:
            pending_location = Location.objects.get(pk=location_id)
        if error_message:
            print(error_message)
        new_studyspace_form = NewStudySpaceForm(request.POST, prefix="new_studyspace")
        if new_studyspace_form.is_valid() and new_studyspace_form.cleaned_data['capacity'] > 0:
            print(location_id)
            pending_space = PendingStudySpace(
                name=new_studyspace_form.cleaned_data['studySpaceName'],
                capacity=new_studyspace_form.cleaned_data['capacity'],
                comments=[new_studyspace_form.cleaned_data['comment']],
                overall_ratings=[int(new_studyspace_form.cleaned_data['overall_rating'])],
                comfort_ratings=[int(new_studyspace_form.cleaned_data['comfort_rating'])],
                noise_level_ratings=[int(new_studyspace_form.cleaned_data['noise_level_rating'])],
                crowdedness_ratings=[int(new_studyspace_form.cleaned_data['crowdedness_rating'])],
            )
            if location_id != -1:
                pending_space.content_type = ContentType.objects.get(model="location")
                pending_space.object_id = location_id
            else:
                pending_space.content_type = ContentType.objects.get(model="pendinglocation")
                pending_location.save()
                pending_space.object_id = pending_location.location_id
                print(pending_location)
            if error_message:
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
                print(pending_space)
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
    if settings.DEBUG:
        json_response = {}
        json_response.update(__load_subprocess(Location, 'locations.json', name="location", id_var_name="location_id"))
        json_response.update(__load_subprocess(StudySpace, 'studyspaces.json', name="studyspace", id_var_name="studyspace_id"))
        return JsonResponse(json_response, safe=True)
    else:
        return HttpResponseNotFound()


def __load_subprocess(cls, filename, name="object", name_plural=None, id_var_name="id"):
    if name_plural is None:
        name_plural = name + "s"
    with open(filename) as json_file:
        try:
            objects = json.load(json_file)
        except JSONDecodeError as e:
            e.msg += "Formatting error with json file"
            raise e

    added_objects = []
    for object_dict in objects:
        if cls.objects.filter(**{f'{id_var_name}': int(object_dict[f'{id_var_name}'])}).count() == 0:
            obj = cls()
            for k, v in object_dict.items():
                setattr(obj, k, v)
            obj.save()
            added_objects.append(getattr(obj, id_var_name))
    json_response = None
    if len(added_objects) == 0:
        json_response = dict({"Warning": f"No {name_plural} added. Already in database"})
    elif len(added_objects) == 1:
        json_response = dict({"Success": f"Added {name} {added_objects[0]}"})
    else:
        json_response = dict({"Success": f"Added {name_plural} {str(added_objects).replace('[', '').replace(']', '')}"})
    json_response = {f'{name.title()}': f'{json_response}'}
    return json_response


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
    """
    Render the review form for a specific study space.

    This function retrieves the location ID and ordinal from the request, gets the corresponding study space,
    and renders the 'studyspace_form.html' template with the location ID and study space as context variables.

    If the location ID or ordinal is not provided, the function raises an Http404 error.

    Args:
        request: The HTTP request.

    Returns:
        An HttpResponse object with the rendered text of the 'studyspace_form.html' template.
    """
    
    location_id = get_variable(request, 'location')
    location_ordinal = get_variable(request, 'space')
    if location_id and location_ordinal:
        studyspace_obj = get_studyspace_by_ordinal(location_id, location_ordinal)
        return render(request, 'studyspots/studyspace_form.html',
                      {'location_id': location_id, 'studyspace': studyspace_obj})
    raise Http404()


# method to process a review for a study spot and update database
def process_studyspace_review(request):
    """
    Process a review for a study spot and update the database.

    This function retrieves the location ID and ordinal from the request, gets the corresponding study space,
    updates its ratings and comments based on the POST data, and saves the changes to the database.

    If the location ID or ordinal is not provided, or if the request method is not POST, the function raises an Http404 error.

    Args:
        request: The HTTP request.

    Returns:
        A redirect to the 'get_spot' view for the specified location and study space.
    """
    
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


@login_required
def approve(request):
    pending_studyspaces = PendingStudySpace.objects.all()
    context = {
        'pending_studyspaces': pending_studyspaces,
    }
    return render(request, 'studyspots/pending.html', context)


def pending_detail(request, studyspace_id):
    pending_studyspace = get_object_or_404(PendingStudySpace, pk=studyspace_id)
    pending_location = None
    if pending_studyspace.content_type.model == 'pendinglocation':
        pending_location_id = pending_studyspace.object_id
        pending_location = get_object_or_404(PendingLocation, pk=pending_location_id)
    context = {
        'pending_studyspace': pending_studyspace,
        'pending_location': pending_location,
    }
    return render(request, 'studyspots/pendingDetail.html', context)


def approve_pending(request, studyspace_id):
    pending_studyspace = get_object_or_404(PendingStudySpace, pk=studyspace_id)
    if pending_studyspace.content_type.model == 'pendinglocation':
        new_location = Location(
            name=pending_studyspace.location.name,
            location_type=pending_studyspace.location.location_type,
            on_grounds=pending_studyspace.location.on_grounds,
            lat=pending_studyspace.location.lat,
            lng=pending_studyspace.location.lng,
        )
        new_location.save()
        new_studyspace = StudySpace(
            location_id=new_location,
            name=pending_studyspace.name,
            capacity=pending_studyspace.capacity,
            comments=pending_studyspace.comments,
            overall_ratings=pending_studyspace.overall_ratings,
            comfort_ratings=pending_studyspace.comfort_ratings,
            noise_level_ratings=pending_studyspace.noise_level_ratings,
            crowdedness_ratings=pending_studyspace.crowdedness_ratings,
        )
        new_studyspace.save()
        pending_studyspace.delete()
        pending_studyspace.location.delete()
        return render(request, 'studyspots/reviewConfirmation.html')
    else:
        new_studyspace = StudySpace(
            location_id=pending_studyspace.location,
            name=pending_studyspace.name,
            capacity=pending_studyspace.capacity,
            comments=pending_studyspace.comments,
            overall_ratings=pending_studyspace.overall_ratings,
            comfort_ratings=pending_studyspace.comfort_ratings,
            noise_level_ratings=pending_studyspace.noise_level_ratings,
            crowdedness_ratings=pending_studyspace.crowdedness_ratings,
        )
        new_studyspace.save()
        pending_studyspace.delete()
        return render(request, 'studyspots/reviewConfirmation.html')


def reject_pending(request, studyspace_id):
    pending_studyspace = get_object_or_404(PendingStudySpace, pk=studyspace_id)
    if pending_studyspace.content_type.model == 'pendinglocation':
        pending_location_id = pending_studyspace.object_id
        pending_location = get_object_or_404(PendingLocation, pk=pending_location_id)
        pending_location.delete()
        pending_studyspace.delete()
    else:
        pending_studyspace.delete()

    return render(request, 'studyspots/reviewConfirmation.html')


def reviewConfirmation(request):
    return render(request, 'studyspots/reviewConfirmation.html')


def change_location(request, studyspace_id):
    pending_studyspace = get_object_or_404(PendingStudySpace, pk=studyspace_id)
    if pending_studyspace.content_type.model == 'pendinglocation':
        pending_location_id = pending_studyspace.object_id
        pending_location = get_object_or_404(PendingLocation, pk=pending_location_id)
        if request.method == 'POST':
            new_studyspace_form = NewStudySpaceForm(request.POST, prefix='pending_studyspace')
            new_location_form = NewLocationForm(request.POST, prefix='pending_location')
            if new_studyspace_form.is_valid():
                new_location_form.is_valid()
                edit_pending_location = PendingLocation(
                    name=new_location_form.cleaned_data['locationName'],
                    location_type=new_location_form.cleaned_data['location_type'],
                    on_grounds=new_location_form.cleaned_data['on_grounds'],
                    lat=pending_location.lat,
                    lng=pending_location.lng,
                )
                edit_pending_location.save()
                pending_location.delete()
                edit_pending_space = PendingStudySpace(
                    content_type=ContentType.objects.get_for_model(edit_pending_location),
                    object_id=edit_pending_location.pk,
                    name=new_studyspace_form.cleaned_data['studySpaceName'],
                    capacity=new_studyspace_form.cleaned_data['capacity'],
                    comments=[new_studyspace_form.cleaned_data['comment']],
                    overall_ratings=[new_studyspace_form.cleaned_data['overall_rating']],
                    comfort_ratings=[new_studyspace_form.cleaned_data['comfort_rating']],
                    noise_level_ratings=[new_studyspace_form.cleaned_data['noise_level_rating']],
                    crowdedness_ratings=[new_studyspace_form.cleaned_data['crowdedness_rating']],
                )
                edit_pending_space.save()
                pending_studyspace.delete()
                return redirect('studyspots:reviewConfirmation')
    else:
        pending_location = None
        new_location_form = None
        if request.method == 'POST':
            new_studyspace_form = NewStudySpaceForm(request.POST)
            if new_studyspace_form.is_valid():
                edit_pending_space = PendingStudySpace(
                    content_type=ContentType.objects.get_for_model(pending_studyspace.location),
                    object_id=pending_studyspace.location.pk,
                    name=new_studyspace_form.cleaned_data['studySpaceName'],
                    capacity=new_studyspace_form.cleaned_data['capacity'],
                    comments=[new_studyspace_form.cleaned_data['comment']],
                    overall_ratings=[new_studyspace_form.cleaned_data['overall_rating']],
                    comfort_ratings=[new_studyspace_form.cleaned_data['comfort_rating']],
                    noise_level_ratings=[new_studyspace_form.cleaned_data['noise_level_rating']],
                    crowdedness_ratings=[new_studyspace_form.cleaned_data['crowdedness_rating']],
                )
                edit_pending_space.save()
                pending_studyspace.delete()
                return redirect('studyspots:reviewConfirmation')
    context = {
        'new_studyspace_form': new_studyspace_form,
        'pending_studyspace': pending_studyspace,
        'new_location_form': new_location_form,
        'pending_location': pending_location,
               }
    return render(request, 'studyspots/change_location.html', context)

