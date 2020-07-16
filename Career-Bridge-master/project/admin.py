from django.contrib import admin
from .models import Project, Milestones, Rating

# Register your models here.

admin.site.register(Project)
admin.site.register(Milestones)
admin.site.register(Rating)