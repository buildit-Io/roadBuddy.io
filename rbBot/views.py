from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import View
from django.template import loader
from .models import PlanningSession, User, Temp, Route
import json
import os
import rbBot.botbrain.logic as Logic
import rbBot.botbrain.reply as Reply
try:
    # HERE API Keys
    import rb.settings._secrets as secure
    SECRET_KEY_3 = secure.SECRET_KEY_3
    SECRET_KEY_4 = secure.SECRET_KEY_4
except ImportError:
    SECRET_KEY_3 = "error_token"
    SECRET_KEY_4 = "error_token"

def index(request):
    return HttpResponse("Hello, world. This is the bot app.")

def route(request):
    print("4")
    template = loader.get_template("route.html")
    routeQuery = Route.objects.filter(id=request.GET['route'])
    if routeQuery.exists():
        info = routeQuery.get().info
        context = {
            'route' :  info['routes'][0],
            'apiKey' : os.getenv("SECRET_KEY_3", SECRET_KEY_3),
        }
        return HttpResponse(template.render(context, request))
    return JsonResponse({"ERROR": "Route Does Not Exists"})

def settings(request):
    template = loader.get_template("settings.html")
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        print(search_id)
        return HttpResponse("no such user")  
    else:
        return HttpResponse(template.render({}, request))

def organiser(request):
    template = loader.get_template("organiser.html")
    routeQuery = Route.objects.filter(id=request.GET['route'])
    if routeQuery.exists():
        info = routeQuery.get().destinations
        context = {
            'dests' :  info
        }
        return HttpResponse(template.render(context, request))
    return JsonResponse({"ERROR": "Route Does Not Exists"})
    
# https://api.telegram.org/bot<token>/setWebhook?url=<url>
class rbHookView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "POST request processed"})

    def post(self, request, *args, **kwargs):
        telegramData = json.loads(request.body)
        ##################
        # DEBUGGING LINE #
        ##################
        print(telegramData)
        ########################
        # COMMENT OUT TO RESET #
        ########################
        self.postHandler(telegramData)
        return JsonResponse({"ok": "POST request processed"})
    
    def postHandler(self,data):
        
        if 'callback_query' in data:
            query = data['callback_query']
            self.callbackHandler(query)
        elif 'message' in data:
            message = data['message']
            if 'text' not in message:
                Reply.no_reply(message['from']['id'])
                return
            else:
                key = message['text']

            if key[1:] != "start":
                sender = message['from']['id']
                if Logic.hasUser(User,sender):
                    if Logic.isActive(sender):
                       pass 
                elif Logic.hasUser(Temp,sender):
                   pass
                else:
                    Reply.no_reply(sender)
                    return

            if 'entities' in message:
                if message['entities'][0]['type'] == "bot_command":
                    self.commandHandler(key[1:],message)
            else:
                self.replyHandler(key,message)
        else: 
            return

    def commandHandler(self,command,message):
        
        sender = message['from']['id']
        message_id = message['message_id']
        target = message['chat']['id']

        if not Logic.hasUser(User,sender):
            Logic.addTmp(message)
            Reply.registerQuery(target)
            return

        if command == "start":
            Reply.welcome(target,sender)
            Reply.provideChoice(target)
            Logic.activate(message_id,sender)
        elif command == "plan":
            return 
        elif command == "quit":
            if Logic.isPlanning(sender):
                Logic.stopPlanning(sender)
                Logic.delPlanningSession(message,-1)
            Reply.commandQuit(target,sender)
            Logic.deactivate(message_id,sender)
        else:
            Reply.no_reply(target)

    def callbackHandler(self, callbackData):
        
        sender = callbackData['from']['id']
        instance = callbackData['id']
        message_id = callbackData['message']['message_id']
        target = callbackData['message']['chat']['id']
        
        #################################
        # TEMPORARY ERROR HANDLING LINE #
        #################################
        if not Logic.hasUser(User,sender):
            Reply.invalidCallback(instance)
            Reply.no_reply(target)
            return

        if message_id <= Logic.getUser(User,sender).latest_message:
            Reply.invalidCallback(instance)
            return
        
        if callbackData['data'] == "plan":
            if Logic.isEditing(sender):
                Logic.stopEditing(sender)
            if Logic.isPlanning(sender):
                Reply.prePlanCallback(instance)
                Reply.prePlanClicked(target,message_id)
            else:
                Logic.startPlanning(sender)
                Logic.addPlanningSession(callbackData,-1)
                Reply.planCallback(instance)
                Reply.planClicked(target,message_id)
        elif callbackData['data'] == "reset_plan_clicked":
            Logic.stopPlanning(sender)
            Logic.delPlanningSession(callbackData,-1)
            Logic.startPlanning(sender)
            Logic.addPlanningSession(callbackData,-1)
            Reply.postResetCallback(instance)
            Reply.planClicked(target,message_id)
        elif callbackData['data'][:9] == "use_saved":
            if Logic.isPlanning(sender):
                Logic.stopPlanning(sender)
                Logic.delPlanningSession(callbackData,0)
            Logic.startPlanning(sender)
            route_id = int(callbackData['data'][10:])
            if callbackData['data'][9] == "_":
                Logic.addPlanningSession(callbackData,route_id)
                Reply.planCallback(instance)
                Reply.useOld(target,message_id,Logic.retrieveDests(sender))
            elif callbackData['data'][9] == "#":
                if Logic.getRoute(sender,route_id).get().logged:
                    Logic.addPlanningSession(callbackData,-1)
                    Logic.duplicateRoute(route_id,sender)
                else:
                    Logic.addPlanningSession(callbackData,route_id)
                Reply.planCallback(instance)
                dests = json.loads(Logic.getRoute(Logic.getUser(User,sender),route_id).get().destinations)
                Reply.useOld(target,message_id,dests)
            else:
                Reply.no_reply(target)
        elif callbackData['data'] == "not_plan":
            Reply.notplanCallback(instance)
            Reply.notplanClicked(target,message_id)
        elif callbackData['data'] == "settings":
            Reply.notplanCallback(instance)
            Reply.notplanClicked(target,message_id)
        elif callbackData['data'] == "plan_help":
            Reply.planHelpCallback(instance)
        elif callbackData['data'] == "resume_plan":
            Reply.resumePlanCallback(instance)
            Reply.resumePlanClicked(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "reset_plan":
            Reply.warningCallback(instance)
            Reply.resetPlanClicked(target,message_id)
        elif callbackData['data'] == "pre_plan":
            Reply.prePlanCallback(instance)
            Reply.prePlanClicked(target,message_id)
        elif callbackData['data'] == "edit":
            if len(Logic.retrieveDests(sender)) < 1:
                Reply.invalidPlanCallback(instance)
                Reply.invalidEditPlanClicked(target,message_id)
            else:
                Logic.startEditing(sender)
                Reply.editCallback(instance)
                Reply.editPlan(sender,target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "edit_dests":
            Reply.editDestsCallback(instance)
            Reply.editDests(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "change_dest" or callbackData['data'][:12] == "change_dest,":
            Reply.changeDestCallback(instance)
            Reply.changeDest(target,message_id)
            if len(callbackData['data']) > 10:
                Logic.setDestChange(callbackData['data'][12:],sender)
        elif callbackData['data'] == "change_dest_next":
            if not Logic.canChange(sender):
                Reply.invalidPlanCallback(instance)
                Reply.noReplacementFound(target,message_id)
            else:
                Reply.warningCallback(instance)
                Reply.changeDestNext(target,message_id)
        elif callbackData['data'] == "confirm_change_dest":
            Reply.confirmDestChangeCallback(instance)
            Logic.replaceInRoute(sender)
            Reply.editDests(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "options":
            Reply.backCallback(instance)
            Reply.backToOptions(target,message_id)
        elif callbackData['data'] == "plan_next":
            if len(Logic.retrieveDests(sender)) < 2:
                Reply.invalidPlanCallback(instance)
                Reply.invalidPlanClicked(target,message_id,Logic.retrieveDests(sender))
            else:
                Reply.warningCallback(instance)
                Reply.preRouting(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "visualise":
            Logic.stopPlanning(sender)
            Logic.confirmRoute(sender)
            Reply.visualiseCallback(instance)
            Reply.visualise(sender,target,message_id)
            Logic.delPlanningSession(callbackData,-1)
        elif callbackData['data'] == "get_saved" or callbackData['data'][:10] == "get_saved#":
            if len(callbackData['data']) > 9:
                Reply.routeDetailsCallback(instance)
                Reply.routeDetails(sender,target,message_id,int(callbackData['data'][10:]))
            else:
                Reply.getSavedCallback(instance)
                Reply.getSaved(sender,target,message_id)
        elif callbackData['data'] == "pre_wipe":
            Reply.warningCallback(instance)
            Reply.preWipe(target,message_id)
        elif callbackData['data'] == "wipe":
            Reply.wipeCallback(instance)
            Logic.wipeData(callbackData)
            Reply.provideChoice(target)
            Logic.activate(message_id,sender)
        elif callbackData['data'] == "pre_quit":
            Reply.warningCallback(instance)
            Reply.preQuit(target,message_id)
        elif callbackData['data'] == "quit":
            if Logic.isPlanning(sender):
                Logic.stopPlanning(sender)
                Logic.delPlanningSession(callbackData,-1)
            Reply.quitCallback(instance)
            Reply.inlineQuit(target,message_id,sender)
            Logic.deactivate(message_id,sender)
        else:
            Reply.no_reply(target)
        
    def replyHandler(self,command,message):
        sender = message['from']['id']
        message_id = message['message_id']
        
        if 'animation' in message or 'document' in message:
            print("sent invalid file")
            Reply.no_reply(sender)
            return

        if Logic.hasUser(User, sender):
            if Logic.isEditing(sender):
                Reply.delete_message(sender,message_id)
                current = User.objects.get(user_id=sender)
                session = PlanningSession.objects.get(user=current)
                oldDest = Logic.retrieveDests(sender)[Logic.getUser(User,sender).key_for_dest]
                if Logic.locExists(message['text']):
                    result = Logic.getResult(message['text'])
                    Logic.logDest(result,sender)
                    Logic.logReplacement(message['text'],sender)
                    Reply.replaceDestValid(session.chat_id,session.message_id,oldDest,message['text'])
                else:
                    Reply.replaceDestInvalid(session.chat_id,session.message_id,[oldDest,message['text']])
            elif Logic.isPlanning(sender):    
                Reply.delete_message(sender,message_id)
                current = User.objects.get(user_id=sender)
                session = PlanningSession.objects.get(user=current)
                if Logic.locExists(message['text']):
                    result = Logic.getResult(message['text'])
                    Logic.logDest(result,sender)
                    Logic.addToRoute(result,message['text'],sender)
                    Reply.addDest(session.chat_id,session.message_id,Logic.retrieveDests(sender))
                else:
                    Reply.invalidDest(session.chat_id,session.message_id,Logic.retrieveDests(sender))
            else:
                Reply.no_reply(sender)
        elif Logic.hasUser(Temp,sender):
            if Logic.isRegistering(message['text']):
                Logic.deleteTmp(message)
                if message['text'] == 'Register':
                    Logic.addUser(message)
                    Reply.registered(sender)
                    Logic.activate(message_id,sender);
                    Reply.provideChoice(sender)
                elif message['text'] == 'Back':
                    Reply.nextTime(sender)
                else:
                    Reply.no_reply(sender)
        else:
            Reply.no_reply(sender)
