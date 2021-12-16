from django.contrib import admin

from .models import Cat, Breed

admin.site.register(Breed)
admin.site.register(Cat)
# Register your models here.
