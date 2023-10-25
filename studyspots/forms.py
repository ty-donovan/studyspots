# forms.py
from django import forms
from location_field.forms.plain import PlainLocationField

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

class LocationForm(forms.Form):
    name = forms.CharField(label='Name of Location', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    on_grounds = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    overall_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    comfort_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    noise_level_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    crowdedness_rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    lat = forms.DecimalField(widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    lng = forms.DecimalField(widget=forms.HiddenInput(attrs={'class': 'form-control'}))
