from django.urls import path, include
from . import views
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView

app_name = "users"
urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("", include("allauth.urls")),
    path("login/", LoginView.as_view(), name="rest_login"),
    path(
        "registration/",
        views.CustomRegisterViewSet.as_view(),
        name=app_name,
    ),
    path(
        "",
        views.UserViewSet.as_view({"get": "list", "post": "create"}),
        name=app_name,
    ),
    path(
        "credits/",
        views.UserCreditViewSet.as_view({"get": "list", "post": "create"}),
        name=app_name,
    ),
    path(
        "reservations/",
        views.UserReservationViewSet.as_view(
            {"get": "get_reservations", "post": "create"}
        ),
        name=app_name,
    ),
    path(
        "reservations/<int:pk>",
        views.UserReservationViewSet.as_view(
            {"get": "retrieve", "put": "put_reservation_cancel", "delete": "destroy"}
        ),
        name=app_name,
    ),
]
