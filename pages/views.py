from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class ComingSoonPageView(TemplateView):
    template_name = "pages/coming_soon.html"