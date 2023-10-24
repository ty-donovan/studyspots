from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    path("", views.index, name="index"),
    path("map/", views.map, name="map"),
    path("add/", views.add, name="add"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="login"),
    path("load/", views.load, name="load"),
    path("load/spot/<int:location_id>", views.get_spot_data, name="get_spot_data"), #hi 
]
