from django.contrib import admin
from .models import User, PlanningSession, Location, Route

# Register your models here.
 
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Route)
admin.site.register(PlanningSession)