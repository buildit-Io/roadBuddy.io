from django.core.exceptions import ObjectDoesNotExist 
from .models import User, Temp, PlanningSession, Location, Route 
# hid keys in local _secrets.py NOT PUSHED TO GITHUB
try:
    # HERE API Keys
    import rb.settings._secrets as secure
    SECRET_KEY_3 = secure.SECRET_KEY_3
    SECRET_KEY_4 = secure.SECRET_KEY_4
except ImportError:
    SECRET_KEY_3 = "error_token"
    SECRET_KEY_4 = "error_token"

def isActive(sender):
    x = User.objects.get(user_id=sender)
    return x.is_started

def getTarget(data):
    return data['from']['id']

def hasUser(model,key):
    try:
        model.objects.get(user_id=key)
        return True
    except ObjectDoesNotExist:
        return False

def isRegistering(response):
    if response == "Register" or response == "Back":
        return True
    else:
        return False

def addTmp(message):
    x = Temp(
        user_id = message['from']['id'],
    )
    x.save()

def deleteTmp(message):
    x = Temp.objects.get(user_id=message['from']['id'])
    x.delete()

def addUser(message):
    try:
        x = User(
            user_id = message['from']['id'],
            first_name = message['from']['first_name'],
            last_name = message['from']['last_name'],
            username = message['from']['username'],
        )
    except KeyError:
        x = User(
            user_id = message['from']['id'],
            first_name = message['from']['first_name'],
            username = message['from']['username'],
        )
    x.save()

def activate(user,message_id):
    if not user.is_started:
        user.is_started = True
    user.latest = message_id
    user.save()

def deactivate(user,message_id):
    if user.is_started:
        user.is_started = False
    user.latest = message_id
    user.save()

def addPlanningSession(callbackData):
    x = PlanningSession(
        chat_id = callbackData['message']['chat']['id'],
        message_id = callbackData['message']['message_id'],
        instance = callbackData['id'],
        message = callbackData['message']['text'],
    )
    owner = User.objects.get(user_id=callbackData['from']['id'])
    x.user = owner
    x.save()

def delPlanningSession(callbackData):
    x = PlanningSession.objects.get(user=User.objects.get(user_id=callbackData['from']['id']))
    x.delete()

def isPlanning(user):
    return User.objects.filter(user_id=user).get().is_planning;

def startPlanning(user):
    user.is_planning = True;
    user.save()

def stopPlanning(user):
    user.is_planning = False;
    user.save()

def isValidDest(input):
    pass

