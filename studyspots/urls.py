from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    path("", views.index, name="index"),
    path("map/", views.map, name="map"),
    path("add/", views.add, name="add"),
    path("add/location_<int:location_id>/", views.add, name="add_with_location"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="login"),
    path("load/", views.load, name="load"),
    path("location_<int:location_id>/space_<int:location_ordinal>/", views.get_studyspace_data, name="get_studyspace_data"),
    path("location_<int:location_id>/", views.get_location_data, name="get_location_data"),
]
