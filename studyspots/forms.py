# forms.py
from django import forms
from location_field.forms.plain import PlainLocationField
from .models import Location

TYPE_CHOICES = [
    ('Library', 'Library'),
    ('Academic Building', 'Academic Building'),
    ('Outdoor', 'Outdoor'),
    ('Business', 'Business'),
    ('Other', 'Other'),
]

RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]

class SelectExistingLocationForm(forms.Form):
    existing_location = forms.ModelChoiceField(
        queryset=Location.objects.order_by('name'),
        label='Select an existing location',
        empty_label='Select a location',
        required=False
    )



class newLocationForm(forms.Form):
    # These are the fields to add a location
    locationName = forms.CharField(
        label='Name of Location',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True  # Mark the field as required
    )
    location_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    on_grounds = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    lat = forms.DecimalField(
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
        required=True  # Mark the field as required
    )
    lng = forms.DecimalField(
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
        required=True  # Mark the field as required
    )
    # These are the fields to add a spot

    spotName = forms.CharField(
        label='Name of Spot',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True  # Mark the field as required
    )
    capacity = forms.IntegerField(
        label='Capacity',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_value=1000,
        required=True  # Mark the field as required
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a description or comment about this spot!'})
        ,
        required=False
    )
    overall_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    comfort_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    noise_level_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    crowdedness_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )



class existingLocationForm(forms.Form):
    
    spotName = forms.CharField(
        label='Name of Spot',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True  # Mark the field as required
    )
    capacity = forms.IntegerField(
        label='Capacity',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_value=1000,
        required=True  # Mark the field as required
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a description or comment about this spot!'})
        ,
        required=False
    )
    overall_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    comfort_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    noise_level_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )
    crowdedness_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True  # Mark the field as required
    )