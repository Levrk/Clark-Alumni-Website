from django.urls import path

from meta import views

urlpatterns = [
    path("", views.home_screen, name="home"),
]
