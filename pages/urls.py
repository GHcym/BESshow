from django.urls import path

from .views import HomePageView, AboutPageView, ComingSoonPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("coming-soon/", ComingSoonPageView.as_view(), name="coming_soon"),
]