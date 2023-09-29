from django.urls import path

from . import views

app_name = "studyspots"
urlpatterns = [
    path("", views.index, name="index"),
    path("map/", views.map, name="map"),
    path("login/", views.login, name="login"),
]