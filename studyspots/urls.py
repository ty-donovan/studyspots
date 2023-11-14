from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "studyspots"
urlpatterns = [
    # path("", views.index, name="index"),
    re_path(r'^$', views.map, name="map"),
    re_path(r'^map/$', views.map_redirect, name="map_redirect"),
    re_path(r'^add/$', views.add, name="add"),
    path("approve/", views.approve, name="approve"),
    path("load/", views.load, name="load"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", views.profile, name="login"),
    re_path(r'^spot/$', views.get_spot, name="get_spot"),
    re_path(r'^review_spot/$', views.review_studyspace, name="review_studyspace"),
    re_path(r'^process_review/$', views.process_studyspace_review, name="process_studyspace_review"),
    path('pending_detail/<int:studyspace_id>/', views.pending_detail, name='pending_detail'),
    path('approve_pending/<int:studyspace_id>/', views.approve_pending, name='approve_pending'),
    path('reject/<int:studyspace_id>/', views.reject_pending, name='reject_pending'),
    path('change_location/<int:studyspace_id>/', views.change_location, name='change_location'),
    path("review_confirmation/", views.reviewConfirmation, name="reviewConfirmation"),
]
