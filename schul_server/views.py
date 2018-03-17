from django.views.generic.list import ListView
from accounts import models

class HomePage(ListView):
    template_name = "index.html"
    model = models.Thema
    queryset = models.Thema.objects.order_by('-erstellt')[:3]
