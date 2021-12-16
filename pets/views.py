from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from pets.models import Pet, Type
#from autos.forms import MakeForm

# Create your views here.


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        tc = Type.objects.all().count()
        pl = Pet.objects.all()

        ctx = {'type_count': tc, 'pet_list': pl}
        return render(request, 'pets/pet_list.html', ctx)


class TypeView(LoginRequiredMixin, View):
    def get(self, request):
        tl = Type.objects.all()
        ctx = {'type_list': tl}
        return render(request, 'pets/type_list.html', ctx)


class TypeCreate(LoginRequiredMixin, CreateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('pets:all')

class TypeUpdate(LoginRequiredMixin, UpdateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('pets:all')


class TypeDelete(LoginRequiredMixin, DeleteView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('pets:all')


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = '__all__'
    success_url = reverse_lazy('pets:all')


class PetUpdate(LoginRequiredMixin, UpdateView):
    model = Pet
    fields = '__all__'
    success_url = reverse_lazy('pets:all')


class PetDelete(LoginRequiredMixin, DeleteView):
    model = Pet
    fields = '__all__'
    success_url = reverse_lazy('pets:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview