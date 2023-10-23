from django.db import models


class Location(models.Model):
    # variable as identifier for each location
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # this variable tells whether the building is on grounds or not. note: the prepopulated ones will all be set to true
    on_grounds = models.BooleanField(default=False)
    # these are the location types that we have as of now, may want to change later. I added a default "Other" to
    # account for buildings/locations such as the Rotunda or a rec center that doesn't fit as nicely into a category
    TYPE_CHOICES = [
        ('Library', 'Library'),
        ('Academic Building', 'Academic Building'),
        ('Outdoor', 'Outdoor'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]
    location_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Other')
    # the address of the location in written form
    address = models.CharField(max_length=255)
    # coordinates is stored as a string with lat and long seperated by a comma
    coordinates = models.CharField(max_length=50)
    # want to support images if this is something we choose to add later. note: this directory does not exist yet
    #image = models.ImageField(upload_to='study_location_images/', null=True, blank=True)
    # We don't have links for any of the buildings rn. Could be nice to give option for businesses to put website.
    # could also be a link to the Google Maps location if we want to change it to that (it would be easy to generate
    # this url based on the coordinates/address)
    link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



def calculate_average_rating(ratings_list):
    if not ratings_list:
        return None
    total_ratings = sum(ratings_list)
    num_ratings = len(ratings_list)
    if num_ratings == 0:
        return None
    return total_ratings / num_ratings


class StudySpace(models.Model):
    # unique identifier for each space entry
    space_id = models.AutoField(primary_key=True)
    # variable to associate the space with an existing Location
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # these are all the types I could think of. Might want to add others later
    TYPE_CHOICES = [
        ('Classroom', 'Classroom'),
        ('Group Study Room', 'Group Study Room'),
        ('Conference Room', 'Conference Room'),
        ('Table', 'Table'),
        ('Public Area', 'Public Area'),
        ('Other', 'Other'),
    ]
    space_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Other')
    # comments is where we'll have a list of comments or written reviews. can be thought of as a sort of discussion
    # space each comment will be saved in this list as a tuple in format ("userID", "user's comment here") ex (
    # "user1234", "this place is great!")
    comments = models.JSONField(default=list)
    reservable = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField()
    # the overall rating for the space as a whole.
    # Each rating (the next 4 fields) will be saved in this list as a  tuple: ("userID", int(rating)) ex ("user1234", 3)
    overall_ratings = models.JSONField(default=list)
    comfort_ratings = models.JSONField(default=list)
    noise_level_ratings = models.JSONField(default=list)
    crookedness_ratings = models.JSONField(default=list)
    # If it is reservable, the link will be to the reserving page (see spreadsheet for these links).
    # If not reservable, this field should probably just stay empty
    link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_overall_rating(self):
        return calculate_average_rating(self.overall_ratings)

    def calculate_comfort_rating(self):
        return calculate_average_rating(self.comfort_ratings)

    def calculate_noise_level_rating(self):
        return calculate_average_rating(self.noise_level_ratings)

    def calculate_crookedness_rating(self):
        return calculate_average_rating(self.crookedness_ratings)
