from django.contrib import admin
from .models import Desprendibles, Employees

# Register your models here.
admin.site.register(Employees),
admin.site.register(Desprendibles)