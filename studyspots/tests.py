from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


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





