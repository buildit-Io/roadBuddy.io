from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import PlanningSession, User, Temp, Route
import json
import rbBot.botbrain.logic as Logic
import rbBot.botbrain.reply as Reply

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
        ########################
        # COMMENT OUT TO RESET #
        ########################
        # self.postHandler(telegramData)
        return JsonResponse({"ok": "POST request processed"})
    
    def postHandler(self,data):
        
        if 'callback_query' in data.keys():
            query = data['callback_query']
            self.callbackHandler(query)
        elif 'message' in data.keys():
            message = data['message']
            key = message['text']

            if key[1:] != "start":
                sender = Logic.getTarget(message)
                if Logic.hasUser(User,sender):
                    if Logic.isActive(sender):
                       pass 
                elif Logic.hasUser(Temp,sender):
                   pass
                else:
                    Reply.no_reply(sender)
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

        if not Logic.hasUser(User,sender):
            Logic.addTmp(message)
            Reply.registerQuery(target)
            return

        if command == "start":
            Reply.welcome(target,sender)
            Reply.provideChoice(target)
            Logic.activate(message_id,sender)
        elif command == "quit":
            if Logic.isPlanning(sender):
                Logic.stopPlanning(sender)
                Logic.delPlanningSession(callbackData)
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
        
        if callbackData['data'] == "plan" or callbackData['data'] == "reset_plan_clicked":   
            if callbackData['data'] == "reset_plan_clicked":
                Reply.postResetCallback(instance)
            if Logic.isPlanning(sender):
                Reply.prePlanCallback(instance)
                Reply.prePlanClicked(target,message_id)
            else:
                Logic.startPlanning(sender)
                Logic.addPlanningSession(callbackData)
                Reply.planCallback(instance)
                Reply.planClicked(target,message_id)
        elif callbackData['data'] == "not_plan":
            Reply.notplanCallback(instance)
            Reply.notplanClicked(target,message_id)
        elif callbackData['data'] == "plan_help":
            Reply.planHelpCallback(instance)
        elif callbackData['data'] == "resume_plan":
            Reply.resumePlanCallback(instance)
            Reply.resumePlanClicked(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "reset_plan":
            Logic.stopPlanning(sender)
            Logic.delPlanningSession(callbackData)
            Reply.warningCallback(instance)
            Reply.resetPlanClicked(target,message_id)
        elif callbackData['data'] == "pre_plan":
            Reply.prePlanCallback(instance)
            Reply.prePlanClicked(target,message_id)
        elif callbackData['data'] == "edit_plan": #include an edit plan options
            Reply.editCallback(instance)
            Reply.editPlan(target,message_id)
        elif callbackData['data'] == "options":
            Reply.backCallback(instance)
            Reply.backToOptions(target,message_id)
        elif callbackData['data'] == "plan_next":
            Reply.warningCallback(instance)
            Reply.preRouting(target,message_id,Logic.retrieveDests(sender))
        elif callbackData['data'] == "visualise":
            Logic.stopPlanning(sender)
            Logic.confirmRoute(sender)
            ##################################################
            # TEMPORARY DO NOT RESPECT SEQUENTIAL PROCESSING #
            ##################################################
            # Logic.delPlanningSession(callbackData)
            Reply.visualiseCallback(instance)
            Reply.visualise(target,message_id)
            #########################################
            # SHIFTED TO BE LAST MESSAGE TO PROCESS #
            #########################################
            Logic.delPlanningSession(callbackData)
        elif callbackData['data'] == "get_saved":
            Reply.naCallback(target)
        elif callbackData['data'] == "wipe":
            Reply.naCallback(target)
        elif callbackData['data'] == "pre_quit":
            Reply.warningCallback(instance)
            Reply.preQuit(target,message_id)
        elif callbackData['data'] == "quit":
            if Logic.isPlanning(sender):
                Logic.stopPlanning(sender)
                Logic.delPlanningSession(callbackData)
            Reply.quitCallback(instance)
            Reply.inlineQuit(target,message_id,sender)
            Logic.deactivate(message_id,sender)
        else:
            Reply.no_reply(target)
        
    def replyHandler(self,command,message):
        sender = message['from']['id']
        message_id = message['message_id']
        
        if Logic.hasUser(User, sender):
            Reply.delete_message(sender,message_id)
            if Logic.isPlanning(sender):    
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

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "POST request processed"})
