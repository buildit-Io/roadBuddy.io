import django_heroku
from .base import *

DEBUG = True;

# DO NOT TOUCH IMPORT LINE TO WORK OUT OF THE BOX WITH HEROKU
django_heroku.settings(locals())