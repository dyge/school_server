from django.views.generic.list import ListView
from django.views.generic import TemplateView
from accounts import models

class HomePage(ListView):
    template_name = "index.html"
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')[:3]

class AboutView(TemplateView):
    template_name = 'about.html'
