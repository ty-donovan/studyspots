from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from studyspots.models import *


class LocationModelTests(TestCase):
    def test_attributes(self):
        new_location = Location(
            name="Clem",
            location_type="LIBRARY",
            address="Clem Road",
            lat=12.345,
            lng=-54.321,
            on_grounds=True
        )
        self.assertEqual(new_location.location_id, new_location.pk)
        self.assertEqual(new_location.name, "Clem")
        self.assertEqual(new_location.location_type, "LIBRARY")
        self.assertEqual(new_location.address, "Clem Road")
        self.assertEqual(new_location.lat, 12.345)
        self.assertEqual(new_location.lng, -54.321)
        self.assertTrue(new_location.on_grounds)

    def test_coordinates(self):
        new_location = Location(lat=34.1094, lng=98.34568)
        self.assertEqual(new_location.coordinates, {'lat': 34.1094, 'lng': 98.34568})

    def test_str(self):
        new_location = Location(name='Clem')
        self.assertEqual(str(new_location), 'Clem')


class PendingLocationModelTests(TestCase):
    def test_attributes(self):
        new_pendinglocation = PendingLocation(
            name='Clark',
            location_type='Outdoor',
            address='Clark Court',
            lat=-24.680,
            lng=98.76500,
            on_grounds=False,
        )
        self.assertEqual(new_pendinglocation.location_id, new_pendinglocation.pk)
        self.assertEqual(new_pendinglocation.name, "Clark")
        self.assertEqual(new_pendinglocation.location_type, "Outdoor")
        self.assertEqual(new_pendinglocation.address, "Clark Court")
        self.assertEqual(new_pendinglocation.lat, -24.680)
        self.assertEqual(new_pendinglocation.lng, 98.76500)
        self.assertFalse(new_pendinglocation.on_grounds)

    def test_coordinates(self):
        location = Location(lat=22.223, lng=55.667)
        self.assertEqual(location.coordinates, {'lat': 22.223, 'lng': 55.667})

    def test_str(self):
        new_pendinglocation = PendingLocation(name='Clark Hall')
        self.assertEqual(str(new_pendinglocation), 'Clark Hall')


class StudySpaceModelTests(TestCase):
    def test_attributes(self):
        new_location = Location(name="Library")
        new_studyspace = StudySpace(
            location_id=new_location,
            name='Clem 22',
            space_type='Classroom',
            capacity=30,
            comments='nice classroom',
            overall_ratings='★ Would Not Recommend',
            comfort_ratings='Very Uncomfortable',
            noise_level_ratings='Extremely Noisy', 
            crowdedness_ratings='Overcrowded',
            reservable=True,
        )
        self.assertEqual(new_studyspace.studyspace_id, new_studyspace.pk)
        self.assertEqual(new_studyspace.location_id, new_location)
        self.assertEqual(new_studyspace.name, 'Clem 22')
        self.assertEqual(new_studyspace.space_type, 'Classroom')
        self.assertEqual(new_studyspace.capacity, 30)
        self.assertEqual(new_studyspace.comments, 'nice classroom')
        self.assertEqual(new_studyspace.overall_ratings, '★ Would Not Recommend')
        self.assertEqual(new_studyspace.comfort_ratings, 'Very Uncomfortable')
        self.assertEqual(new_studyspace.noise_level_ratings, 'Extremely Noisy')
        self.assertEqual(new_studyspace.crowdedness_ratings, 'Overcrowded')
        self.assertTrue(new_studyspace.reservable)

    def test_str(self):
        new_studyspace = StudySpace(name='Clem 10')
        self.assertEqual(str(new_studyspace), 'Clem 10')

    def test_calculate(self):
        new_studyspace = StudySpace(overall_ratings=[1, 2, 3])
        overall_rating = new_studyspace.calculate_overall_rating()
        self.assertEqual(overall_rating, 2.0)
        self.assertNotEqual(overall_rating, 3.0)


class PendingStudySpaceModelTests(TestCase):
    def test_attributes(self):
        new_location = PendingLocation(name="Lib")
        new_pendingstudyspace = PendingStudySpace(
            object_id=new_location.pk,
            name='Clark 24',
            capacity=55,
            comments='big room',
            overall_ratings=4,
            comfort_ratings=3,
            noise_level_ratings=2,
            crowdedness_ratings=1,
            space_type='Group Study Room',
            reservable=False
        )
        self.assertEqual(new_pendingstudyspace.studyspace_id, new_pendingstudyspace.pk)
        self.assertEqual(new_pendingstudyspace.object_id, new_location.pk)
        self.assertEqual(new_pendingstudyspace.name, 'Clark 24')
        self.assertEqual(new_pendingstudyspace.space_type, 'Group Study Room')
        self.assertEqual(new_pendingstudyspace.capacity, 55)
        self.assertEqual(new_pendingstudyspace.comments, 'big room')
        self.assertEqual(new_pendingstudyspace.overall_ratings, 4)
        self.assertEqual(new_pendingstudyspace.comfort_ratings, 3)
        self.assertEqual(new_pendingstudyspace.noise_level_ratings, 2)
        self.assertEqual(new_pendingstudyspace.crowdedness_ratings, 1)
        self.assertFalse(new_pendingstudyspace.reservable)


class AdminModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jane', password='hello123', email='jane@gmail.com')

    def test_create_user(self):
        self.assertTrue(Admin.objects.filter(user=self.user).exists())

    def test_username(self):
        admin = Admin.objects.get(user=self.user)
        self.assertEqual(admin.username, 'jane')

    def test_email(self):
        admin = Admin.objects.get(user=self.user)
        self.assertEqual(admin.user.email, 'jane@gmail.com')

    def test_is_admin(self):
        admin = Admin.objects.get(user=self.user)
        admin.is_admin = True
        self.assertTrue(admin.is_admin)


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='password123')

    def test_redirect_no_login(self):
        response = self.client.get(reverse('studyspots:login'))
        self.assertRedirects(response, '/accounts/login/?next=/login/')

    def test_wrong_login(self):
        self.assertTrue(isinstance(self.user, User))
        login = self.client.login(username="john", password='bluesky321')
        self.assertEqual(login, False)

    def test_correct_login(self):
        self.assertTrue(isinstance(self.user, User))
        login = self.client.login(username='username', password='password123')
        self.assertEqual(login, True)
        
    def test_logout(self):
        response = self.client.get(reverse('studyspots:logout'))
        self.assertRedirects(response, '/')


class MapViewTests(TestCase):
    def test_load_map(self):
        response = self.client.get(reverse('studyspots:map'))
        self.assertTemplateUsed(response, 'studyspots/map.html')
        self.assertEqual(response.context['key'], settings.GOOGLE_API_KEY)
        