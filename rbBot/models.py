from django.db import models

# boilerplate
    
def routeInfo_default_value(): 
    return { "routes" : [] } 
    
def destinations_default_value(): 
    return {}

# Create your models here.

class Temp(models.Model):
    user_id = models.BigIntegerField(unique=True, primary_key=True)

class User(models.Model):
    user_id     = models.BigIntegerField(unique=True, primary_key=True)
    first_name  = models.CharField(max_length=64, default="null")
    last_name   = models.CharField(max_length=64, default="null")
    username    = models.CharField(max_length=64, default="null")
    is_started    = models.BooleanField(default=True)
    is_planning = models.BooleanField(default=False)
    is_editing = models.BooleanField(default=False)
    planning_route = models.BigIntegerField(default=0)
    latest_message = models.BigIntegerField(blank=True, null=True)
    key_for_dest = models.TextField(max_length=4000,blank=True, null=True)
    new_dest = models.TextField(max_length=4000,blank=True, null=True)
    routes_created = models.IntegerField(default=0)

    class Meta:
        ordering = ['user_id']

    def __str__(self):
        return f'{self.user_id}'

class PlanningSession(models.Model):
    
    chat_id = models.BigIntegerField(unique=True)
    message_id = models.BigIntegerField(unique=True)
    instance = models.BigIntegerField(unique=True)
    message = models.TextField(max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['chat_id']

    def __str__(self):
        return f'Latest Planning Session {self.message_id} by {self.chat_id}'

class Route(models.Model):

    route_id = models.BigIntegerField(default=None)
    # deletes the route when user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destinations = models.JSONField(default=destinations_default_value)
    # empty values stored as none, set to null when planning session is deleted
    current_session = models.ForeignKey(PlanningSession,on_delete=models.SET_NULL, null=True)
    logged = models.BooleanField(default=False)
    info = models.JSONField(default=routeInfo_default_value)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Route #{self.route_id} belonging to {self.user_id}'

class Location(models.Model):
    postal_code  = models.BigIntegerField()
    long_address  = models.TextField(max_length=4000)
    longtitude = models.DecimalField(max_digits = 18, decimal_places = 15)
    latitude = models.DecimalField(max_digits = 17, decimal_places = 15)
    routes = models.ManyToManyField(Route)

    class Meta:
        ordering = ['postal_code']

    def __str__(self):
        return f'Location: long-{self.longtitude};lat-{self.latitude}'