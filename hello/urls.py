from django.urls import path

from . import views

app_name = 'ads'

urlpatterns = [
    # ex: /hello/
    path('', views.IndexView.as_view(), name='index'),
    #path('', views.myview)

    #path('', TemplateView.as_view(template_name='session/main.html')),
    #path('cookie', views.cookie),
    #path('sessfun', views.sessfun),
]

