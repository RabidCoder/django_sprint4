from django.urls import path
from django.views.generic import TemplateView


app_name = 'pages'

urlpatterns = [
    # О проекте.
    path(
        'about/',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about',
    ),
    # Правила.
    path(
        'rules/',
        TemplateView.as_view(template_name='pages/rules.html'),
        name='rules',
    ),
]
