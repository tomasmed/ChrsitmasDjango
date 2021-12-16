from django.urls import path, reverse_lazy
from . import views

app_name = 'solo'

urlpatterns = [
    # ex: /hello/

    path('', views.solo.as_view(), name='all'),
    ]