from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.map, name="map"),
    path("map/", views.map_redirect, name="map_redirect"),
    path("add/", views.add, name="add"),
    path("addNewLocation/", views.non_existing_location, name="addNewLocation"),
    path("add_new_spot/<int:location_id>/", views.add_new_spot, name="add_new_spot"),
    path("add/location_<int:location_id>/", views.add, name="add_with_location"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="login"),
    path("load/", views.load, name="load"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("location_<int:location_id>/", views.get_location_data, name="get_location_data"),
    path("location_<int:location_id>/space_<int:location_ordinal>/", views.get_studyspace_data, name="get_studyspace_data"),
    path("location_<int:location_id>/space_<int:location_ordinal>/review_spot/", views.review_studyspace, name="review_studyspace"),
    path("location_<int:location_id>/space_<int:location_ordinal>/process_review/", views.process_studyspace_review, name="process_studyspace_review"),

]
