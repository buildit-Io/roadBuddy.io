import os 
from .base import * 

# added for out of the box support for django on heroku
import django_heroku

DEBUG = False

# DO NOT TOUCH IMPORT LINE TO WORK OUT OF THE BOX WITH HEROKU
django_heroku.settings(locals())