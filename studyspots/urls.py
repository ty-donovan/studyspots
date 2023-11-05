from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    # path("", views.index, name="index"),
    re_path(r'^$', views.map, name="map"),
    re_path(r'^add/$', views.add, name="add"),
    path("review/", views.review_pending, name="review"),
    path("load/", views.load, name="load"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="login"),
    path("location_<int:location_id>/", views.get_location_data, name="get_location_data"),
    path("location_<int:location_id>/space_<int:location_ordinal>/", views.get_studyspace_data, name="get_studyspace_data"),
    path("location_<int:location_id>/space_<int:location_ordinal>/review_spot/", views.review_studyspace, name="review_studyspace"),
    path("location_<int:location_id>/space_<int:location_ordinal>/process_review/", views.process_studyspace_review, name="process_studyspace_review"),

]
