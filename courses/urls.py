from django.urls import path, include
from . import views

app_name = "courses"
urlpatterns = [
    path(
        "",
        views.UserCourseViewSet.as_view({"get": "list"}),
        name=app_name,
    ),
    path(
        "admin/",
        views.AdminCourseViewSet.as_view({"get": "list", "post": "create"}),
        name=app_name,
    ),
    path(
        "places/",
        views.AdminPlaceViewSet.as_view({"get": "list", "post": "create"}),
        name=app_name,
    ),
    path(
        "reservations/",
        views.AdminReservationViewSet.as_view(
            {"get": "get_reservations", "post": "create"}
        ),
        name=app_name,
    ),
]
