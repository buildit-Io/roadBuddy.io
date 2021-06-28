from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import PlanningSession, User, Temp
from .logic import *
from .interactions import *
import json

def index(request):
    return HttpResponse("Hello, world. This is the bot app.")

# https://api.telegram.org/bot<token>/setWebhook?url=<url>
class rbHookView(View):

    def post(self, request, *args, **kwargs):
        telegramData = json.loads(request.body)
        ##################
        # DEBUGGING LINE #
        ##################
        print(telegramData)
        self.postHandler(telegramData)
        return JsonResponse({"ok": "POST request processed"})
    
    def postHandler(self,data):
        
        if 'callback_query' in data.keys():
            query = data['callback_query']
            self.callbackHandler(query)
        elif 'message' in data.keys():
            message = data['message']
            key = message['text']

            if key[1:] != "start":
                sender = getTarget(message)
                if hasUser(User,sender):
                    if isActive(sender):
                       pass 
                elif hasUser(Temp,sender):
                   pass
                else:
                    no_reply(sender)
                    return

            if (('entities' in message.keys()) and ('bot_command' in message['entities'][0]['type'])):
                self.commandHandler(key[1:],message)
            else:
                self.replyHandler(key,message)
        else: 
            return

    def commandHandler(self,command,message):
        
        sender = message['from']['id']
        message_id = message['message_id']
        target = message['chat']['id']

        if not hasUser(User,sender):
            addTmp(message)
            registerQuery(target)
            return

        if command == "start":
            user = User.objects.filter(user_id=sender).get();
            welcome(target,user)
            provideChoice(target)
            activate(user,message_id)
        elif command == "quit":
            user = User.objects.filter(user_id=sender).get();
            commandQuit(target,user)
            deactivate(user,message_id)
        else:
            no_reply(target)

    def callbackHandler(self, callbackData):
        
        sender = callbackData['from']['id']
        instance = callbackData['id']
        message_id = callbackData['message']['message_id']
        target = callbackData['message']['chat']['id']
        user = User.objects.filter(user_id=sender).get();

        if message_id <= user.latest:
            invalidCallback(instance)
            return
        
        if callbackData['data'] == "plan":
            if not isPlanning:
                startPlanning(user)
                addPlanningSession(callbackData)
            planCallback(instance)
            planClicked(target,message_id)
        elif callbackData['data'] == "not_plan":
            notplanCallback(instance)
            notplanClicked(target,message_id)
        elif callbackData['data'] == "edit_plan":
            editCallback(instance)
            editPlan(target,message_id)
        elif callbackData['data'] == "options":
            if isPlanning(sender):
                stopPlanning(user)
                delPlanningSession(callbackData)
            backCallback(instance)
            backToOptions(target,message_id)
        elif callbackData['data'] == "plan_next":
            preRoutingCallback(instance)
            preRouting(target,message_id)
        elif callbackData['data'] == "visualise":
            stopPlanning(user)
            delPlanningSession(callbackData)
            routeCallback(instance)
            route(target,message_id)
        elif callbackData['data'] == "get_saved":
            pass
        elif callbackData['data'] == "wipe":
            pass
        elif callbackData['data'] == "pre_quit":
            preQuitCallback(instance)
            preQuit(target,message_id)
        elif callbackData['data'] == "quit":
            quitCallback(instance)
            inlineQuit(target,message_id,user)
            deactivate(user,message_id)
        else:
            no_reply(target)
        
    def replyHandler(self,command,message):
        LOCAL_CACHE = []
        sender = message['from']['id']
        message_id = message['message_id']
        if hasUser(User, sender):
            if isPlanning(sender):    
                current = User.objects.get(user_id=sender)
                session = PlanningSession.objects.get(user=current)
                if isValidDest(message['text']):
                    addDest(session.chat_id, session.message_id)
                    addDestCallback(session.instance)
                else:
                    invalidCallback(session.instance)
            else:
                no_reply(sender)
        elif hasUser(Temp,sender):
            if isRegistering(message['text']):
                deleteTmp(message)
                if message['text'] == 'Register':
                    addUser(message)
                    registered(sender)
                    activate(User.objects.filter(user_id=sender).get(),message_id);
                    provideChoice(sender)
                elif message['text'] == 'Back':
                    nextTime(sender)
                else:
                    no_reply(sender)
        else:
            no_reply(sender)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "POST request processed"})
