from django.core.exceptions import ObjectDoesNotExist 
from rbBot.models import User, Temp, PlanningSession, Location, Route 
from decimal import Decimal
# hid keys in local _secrets.py NOT PUSHED TO GITHUB
try:
    # HERE API Keys
    import rb.settings._secrets as secure
    SECRET_KEY_3 = secure.SECRET_KEY_3
    SECRET_KEY_4 = secure.SECRET_KEY_4
except ImportError:
    SECRET_KEY_3 = "error_token"
    SECRET_KEY_4 = "error_token"
import json
import os 
import requests

GEOCODE_URL = "https://geocode.search.hereapi.com/v1/geocode"
ROUTING_URL = "https://router.hereapi.com/v8/routes"
MAPVIEW_URL = "https://image.maps.ls.hereapi.com/mia/1.6/mapview"
GEOCODE_TOKEN = os.getenv("SECRET_KEY_3", SECRET_KEY_3)

def getTarget(data):
    return data['from']['id']

def hasUser(model,search):
    try:
        model.objects.get(user_id=search)
        return True
    except ObjectDoesNotExist:
        return False

def getUser(model,sender):
    return model.objects.get(user_id=sender)

def isActive(sender):
    return getUser(User,sender).is_started

def isRegistering(response):
    if response == "Register" or response == "Back":
        return True
    else:
        return False

def addTmp(message):
    newEntry = Temp(
        user_id = message['from']['id'],
    )
    newEntry.save()

def deleteTmp(message):
    getUser(Temp,message['from']['id']).delete()

def addUser(message):
    newEntry = User(
        user_id = message['from']['id'],
        latest_message = message['message_id']
    )
    lookup = message['from']
    if 'first_name' in lookup:
        newEntry.first_name = lookup['first_name']
    if 'last_name' in lookup:
        newEntry.last_name = lookup['last_name']
    if 'username' in lookup:
        newEntry.username = lookup['username']
    newEntry.save()

def deleteUser(message):
    getUser(User,message['from']['id']).delete()

def activate(message_id,sender):
    user = getUser(User,sender)
    if not user.is_started:
        user.is_started = True
    user.latest_message = message_id
    user.save()

def deactivate(message_id,sender):
    user = getUser(User,sender)
    if user.is_started:
        user.is_started = False
    user.latest_message = message_id
    user.save()

def isPlanning(sender):
    return getUser(User,sender).is_planning;

def addPlanningSession(callbackData):
    currUser = getUser(User,callbackData['from']['id'])
    newEntry = PlanningSession(
        chat_id = callbackData['message']['chat']['id'],
        message_id = callbackData['message']['message_id'],
        instance = callbackData['id'],
        user = currUser,
        message = callbackData['message']['text'],
    )
    newEntry.save()
    newPlanningState(callbackData)

def delPlanningSession(callbackData):
    searchRes = PlanningSession.objects.get(user=getUser(User,callbackData['from']['id']))
    searchRes.delete()
    delUnsavedRoute(callbackData['from']['id'])

def startPlanning(sender):
    user = getUser(User,sender)
    user.is_planning = True;
    user.save()

def stopPlanning(sender):
    user = getUser(User,sender)
    user.is_planning = False;
    user.save()

def getResult(input):
    response = search(input)
    result = json.loads((response.content).decode('UTF-8'))
    return result

def locExists(input):
    if not getResult(input)['items']:
        return False
    else:
        return True

def getLoc(result):
    return Location.objects.filter(
        longtitude = Decimal(str(result['items'][0]['position']['lng'])),
        latitude = Decimal(str(result['items'][0]['position']['lat']))
    )
    

def isNewLoc(result):
    query = getLoc(result)
    if query.exists():
        return False
    else:
        return True

def search(address):
    if type(address) == int and len(address) == 6:
        response = requests.get(
            GEOCODE_URL,
            params={'qq' : "postalode=" + str(address),
                    'apiKey': GEOCODE_TOKEN,
                    'in': 'countryCode:SGP'}
        )
    else:
        response = requests.get(
            GEOCODE_URL,
            params={'q' : str(address),
                    'apiKey': GEOCODE_TOKEN,
                    'in': 'countryCode:SGP'}
        )
    return response

def logDest(result,sender):
    if isNewLoc(result):
        newEntry = Location(
            postal_code  = result['items'][0]['address']['postalCode'],
            long_address  = str(result['items'][0]['address']),
            longtitude = Decimal(str(result['items'][0]['position']['lng'])),
            latitude = Decimal(str(result['items'][0]['position']['lat'])),
        )
        newEntry.save()

def getRoute(user,route_id):
    return Route.objects.filter(user=user,route_id=route_id)

def newPlanningState(callbackData):
    currUser = getUser(User,callbackData['from']['id'])
    currUser.planning_route = currUser.routes_created+1
    currUser.save()
    
def addToRoute(result,locInput,sender):
    currUser = User.objects.get(user_id=sender)
    currSession = PlanningSession.objects.get(user=currUser)
    query = getRoute(currUser,currUser.planning_route)
    if len(query) > 1:
        print("error")
        return
    # This is a new route signal
    if not query.exists():
        dests = json.dumps({1:locInput})
        newRoute = Route(
            route_id = currUser.planning_route,
            user = currUser,
            current_session = currSession,
            destinations = dests
        )
        newRoute.save()
        newQuery = getRoute(currUser,currUser.planning_route)
        currLoc = getLoc(result).get()
        currLoc.routes.add(newQuery.get())
        currLoc.save()
    else:
        loc = getLoc(result).get()
        newRoute = query.get()
        loc.routes.add(newRoute)
        loc.save()
        dests = json.loads(newRoute.destinations)
        dests[len(dests)+1] = locInput
        newRoute.destinations = json.dumps(dests)
        newRoute.save()

def delUnsavedRoute(sender):
    currUser = User.objects.get(user_id=sender)
    currRouteQuery = getRoute(currUser,currUser.planning_route)
    if currRouteQuery.exists():
        currRoute = currRouteQuery.get()
        if not currRoute.logged:
            currRoute.delete()
    else:
        return 

def retrieveDests(sender):
    currUser = User.objects.get(user_id=sender)
    currRouteQuery = getRoute(currUser,currUser.planning_route)
    if currRouteQuery.exists():
        currRoute = currRouteQuery.get()
        return json.loads(currRoute.destinations)
    else:
        return {}

def confirmRoute(sender):
    user = getUser(User,sender)
    user.routes_created += 1;
    user.save()
    routeQuery = getRoute(user,user.planning_route)
    if not routeQuery.exists():
        return
    route = routeQuery.get()
    route.logged = True
    route.save()
    destSet = Location.objects.filter(routes=route).values('latitude','longtitude')
    destList = list(destSet)
    waypointList = []
    for dest in destList:
        waypoint = str(dest['latitude']) + "," + str(dest['longtitude'])
        waypointList.append(waypoint)
    route.info = genRoute(waypointList)
    route.save()

def genRoute(dests):
    if len(dests) > 2:
        routeRequestParams = {
            'return': 'polyline,turnByTurnActions,actions,instructions,travelSummary',
            'routingMode': 'fast',
            'transportMode': 'car',
            'origin': dests[0], 
            'destination': dests[-1],
            'apiKey': GEOCODE_TOKEN,
            'via': dests[1:-1],
        }
        response = requests.get(
            ROUTING_URL,
            params=routeRequestParams
        )
    elif len(dests) == 2:
        routeRequestParams = {
            'return': 'polyline,turnByTurnActions,actions,instructions,travelSummary',
            'routingMode': 'fast',
            'transportMode': 'car',
            'origin': dests[0], 
            'destination': dests[-1],
            'apiKey': GEOCODE_TOKEN,
        }
        response = requests.get(
            ROUTING_URL,
            params=routeRequestParams
        )
    else:
        return
    return response.json()

VISUALISATION_URL = "https://roadbuddy-io.herokuapp.com/rbBot/route/"
LOCAL_VISUALISATION_URL = "https://ef28e92f8e13.ngrok.io/rbBot/route/"
def routeURL(routeId):
    response = requests.get(
        LOCAL_VISUALISATION_URL,
        params= {
            'route' : routeId,
        },
    )
    return str(response.request.url)