from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    path("", views.index, name="index"),
    path("map/", views.map, name="map"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="welcome"),
]
