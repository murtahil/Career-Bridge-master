from django.contrib import admin
from .models import University, Bidding, Service

# Register your models here.

admin.site.register(University)
admin.site.register(Service)
admin.site.register(Bidding)
