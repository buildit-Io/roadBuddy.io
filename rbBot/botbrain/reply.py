import os
import json
from .speech import RESPONSES, REPLY_MATRIX, MARKUP_MATRIX, CALLBACK_MATRIX
import requests
import rbBot.botbrain.logic as Logic
from rbBot.models import User
# hid keys in local _secrets.py NOT PUSHED TO GITHUB
try:
    import rb.settings._secrets as secure
    SECRET_KEY_2 = secure.SECRET_KEY_2
except ImportError:
    SECRET_KEY_2 = "error_token"

TELEGRAM_URL = "https://api.telegram.org/bot"
TOKEN = os.getenv("SECRET_KEY_2", SECRET_KEY_2)

def send_message(selector, message, chat_id):
    data = REPLY_MATRIX[selector]
    data["chat_id"] = chat_id
    data["text"] = message
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/sendMessage", data=data
    )

def no_reply(target):
    return send_message("DEFAULT",RESPONSES["DEFAULT"],target)

def welcome(target,sender):
    user = Logic.getUser(User,sender)
    return send_message("DEFAULT",RESPONSES["WELCOME"](user.first_name,user.last_name),target)

def provideChoice(target):
    return send_message("OPTIONS",RESPONSES["OPTIONS"],target)

def registerQuery(target):
    return send_message("REGISTER_QUERY",RESPONSES["REGISTER_QUERY"],target)

def registered(target):
    return send_message("REMOVE_KEYBOARD",RESPONSES["REGISTERED"],target)

def nextTime(target):
    return send_message("REMOVE_KEYBOARD",RESPONSES["NEXT_TIME"],target)

def answer_callback(selector, message, callback_id):
    data = CALLBACK_MATRIX[selector]
    data["callback_query_id"] = callback_id
    data["text"] = message
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/answerCallbackQuery",data=data
    )

def planHelpCallback(target):
    return answer_callback("INVALID",RESPONSES["PLAN_HELP_CALLBACK"],target)

def planCallback(target):
    return answer_callback("DEFAULT",RESPONSES["PLAN_CALLBACK"],target)

def invalidPlanCallback(target):
    return answer_callback("INVALID",RESPONSES["INVALID_PLAN_CALLBACK"],target)

def prePlanCallback(target):
    return answer_callback("DEFAULT",RESPONSES["WARNING_CALLBACK"],target)

def resumePlanCallback(target):
    return answer_callback("DEFAULT",RESPONSES["PLAN_CALLBACK"],target)

def postResetCallback(target):
    return answer_callback("INVALID",RESPONSES["RESET_CALLBACK"],target)

def getSavedCallback(target):
    return answer_callback("DEFAULT",RESPONSES["GET_SAVED_CALLBACK"],target)

def routeDetailsCallback(target):
    return answer_callback("DEFAULT",RESPONSES["ROUTE_DETAILS_CALLBACK"],target)

def editCallback(target):
    return answer_callback("DEFAULT",RESPONSES["EDIT_CALLBACK"],target)

def editDestsCallback(target):
    return answer_callback("DEFAULT",RESPONSES["EDIT_DESTS_CALLBACK"],target)

def changeDestCallback(target):
    return answer_callback("DEFAULT",RESPONSES["CHANGE_DEST_CALLBACK"],target)

def confirmDestChangeCallback(target):
    return answer_callback("DEFAULT",RESPONSES["CONFIRM_CHANGE_DEST_CALLBACK"],target)

def notplanCallback(target):
    return answer_callback("DEFAULT",RESPONSES["NOTPLAN_CALLBACK"],target)

def backCallback(target):
    return answer_callback("DEFAULT",RESPONSES["BACK_CALLBACK"],target)

def warningCallback(target):
    return answer_callback("DEFAULT",RESPONSES["WARNING_CALLBACK"],target)

def quitCallback(target):
    return answer_callback("DEFAULT",RESPONSES["QUIT_CALLBACK"],target)

def wipeCallback(target):
    return answer_callback("INVALID",RESPONSES["WIPE_CALLBACK"],target)

def invalidCallback(target):
    return answer_callback("INVALID",RESPONSES["INVALID_CALLBACK"],target)

def visualiseCallback(target):
    return answer_callback("DEFAULT",RESPONSES["VISUALISE_CALLBACK"],target)

def naCallback(target):
    return answer_callback("DEFAULT",RESPONSES["NA_CALLBACK"],target)

def edit_message(selector, message, chat_id, message_id):
    data = REPLY_MATRIX[selector]
    data["chat_id"] = chat_id
    data["message_id"] = message_id
    data["text"] = message
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def planClicked(target,message_id):
    return edit_message("PLAN",RESPONSES["PLAN"],target,message_id)

def invalidPlanClicked(target,message_id,dests):
    return edit_message("PLAN",RESPONSES["INVALID_PLAN"](dests),target,message_id)

def invalidEditPlanClicked(target,message_id):
    return edit_message("PLAN",RESPONSES["INVALID_EDIT_PLAN"],target,message_id)

def prePlanClicked(target,message_id):
    return edit_message("PRE_PLAN",RESPONSES["PRE_PLAN"],target,message_id)

def resetPlanClicked(target,message_id):
    return edit_message("PRE_RESET",RESPONSES["PRE_RESET"],target,message_id)

def resumePlanClicked(target,message_id,dests):
    return edit_message("PLAN",RESPONSES["RESUME_PLAN"](dests),target,message_id)

def addDest(target,message_id,dests):
    return edit_message("PLAN",RESPONSES["ADD"](dests),target,message_id)

def useOld(target,message_id,dests):
    return edit_message("PLAN",RESPONSES["RESUME_PLAN"](dests),target,message_id)

def noReplacementFound(target,message_id):
    return edit_message("CHANGE_DEST",RESPONSES["NO_REPLACEMENT"],target,message_id)

def replaceDestValid(target,message_id,oldLoc,newLoc):
    return edit_message("CHANGE_DEST",RESPONSES["VALID_DEST"](oldLoc,newLoc),target,message_id)

def replaceDestInvalid(target,message_id,loc):
    return edit_message("CHANGE_DEST",RESPONSES["INVALID_DEST"](loc),target,message_id)

def invalidDest(target,message_id,dests):
    return edit_message("PLAN",RESPONSES["INVALID_DEST"](dests),target,message_id)

def notplanClicked(target,message_id):
    return edit_message("NOTPLAN",RESPONSES["NOTPLAN"],target,message_id)

def backToOptions(target,message_id):
    return edit_message("BACK_TO_OPTIONS",RESPONSES["OPTIONS"],target,message_id)

def changeDest(target,message_id):
    return edit_message("CHANGE_DEST",RESPONSES["CHANGE_DEST"],target,message_id)

def changeDestNext(target,message_id):
    return edit_message("CHANGE_DEST_NEXT",RESPONSES["CHANGE_DEST_NEXT"],target,message_id)

def preRouting(target,message_id,dests):
    return edit_message("PLAN_NEXT",RESPONSES["PLAN_NEXT"](dests),target,message_id)

def preQuit(target,message_id):
    return edit_message("PRE_QUIT",RESPONSES["PRE_QUIT"],target,message_id)

def preWipe(target,message_id):
    return edit_message("PRE_WIPE",RESPONSES["PRE_WIPE"],target,message_id)

def inlineQuit(target,message_id,sender):
    user = Logic.getUser(User,sender)
    return edit_message("QUIT",RESPONSES["QUIT"](user.first_name,user.last_name),target,message_id)

def commandQuit(target,sender):
    user = Logic.getUser(User,sender)
    return send_message("QUIT",RESPONSES["QUIT"](user.first_name,user.last_name),target)


def editPlan(sender,target,message_id,dests):
    data = REPLY_MATRIX["URL"]
    currUser = Logic.getUser(User,sender)
    routeQuery = Logic.getRoute(currUser,currUser.planning_route)
    if routeQuery.exists():
        url = Logic.orderURL(routeQuery.get().id)
    else:
        defaultRoute = json.dumps(-1)
        url = Logic.orderURL(defaultRoute)
    markup = {
        "inline_keyboard" : [[{"text": "Change Order", "url" : url}],
                             [{"text": "Change Destinations", "callback_data" : "edit_dests"}],
                             [{"text": "Done", "callback_data" : "plan"}],
                             ]
    }
    data["chat_id"] = target
    data["reply_markup"] = json.dumps(markup)
    data["message_id"] = message_id
    data["text"] = RESPONSES["EDIT"](dests)
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def editDests(target,message_id,dests):
    data = REPLY_MATRIX["URL"]
    markup = {
        "inline_keyboard" : [],
    }
    currDests = list(dests.values())
    currKeys = list(dests.keys())
    x = 0
    while x < len(dests):
        markup["inline_keyboard"].append([{"text":currDests[x],"callback_data":f"change_dest,{currKeys[x]}"}])
        x += 1
    markup["inline_keyboard"].append([{"text":"Done","callback_data":"edit"}])
    data["chat_id"] = target
    data["reply_markup"] = json.dumps(markup)
    data["message_id"] = message_id
    data["text"] = RESPONSES["EDIT_DESTS"]
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def getSaved(sender,target,message_id):
    data = REPLY_MATRIX["URL"]
    markup = {
        "inline_keyboard" : [],
    }
    currUser = Logic.getUser(User,sender)
    allRoutesQuery = Logic.getRoute(currUser,-1)
    for routeQuery in allRoutesQuery:
        markup["inline_keyboard"].append([{"text":f"Route No. {routeQuery.route_id}","callback_data":f"get_saved#{routeQuery.route_id}"}])
    markup["inline_keyboard"].append([{"text":"Back","callback_data":"not_plan"}])
    data["chat_id"] = target
    data["reply_markup"] = json.dumps(markup)
    data["message_id"] = message_id
    data["text"] = RESPONSES["GET_SAVED"]
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def routeDetails(sender,target,message_id,route_id):
    data = REPLY_MATRIX["URL"]
    markup = {
        "inline_keyboard" : [],
    }
    currUser = Logic.getUser(User,sender)
    route = Logic.getRoute(currUser,route_id).get()
    url = Logic.routeURL(route.id)
    markup = { "inline_keyboard" : [[{"text": "View Route", "url" : url}],
                                    [{"text": "Edit", "callback_data" : f"use_saved_{route_id}"}],
                                    [{"text": "Cache & Edit", "callback_data" : f"use_saved#{route_id}"}],
                                    [{"text": "Back", "callback_data" : "get_saved"},{"text": "Help", "callback_data" : "route_detail_help"}]
                                   ]
              }
    data["chat_id"] = target
    data["reply_markup"] = json.dumps(markup)
    data["message_id"] = message_id
    currUser = Logic.getUser(User,sender)
    dests = json.loads(route.destinations)
    data["text"] = RESPONSES["ROUTE_DETAILS"](dests)
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def visualise(sender,target, message_id):  
    data = REPLY_MATRIX["URL"]
    currUser = Logic.getUser(User,sender)
    routeQuery = Logic.getRoute(currUser,currUser.planning_route)
    print("1")
    if routeQuery.exists():
        print("2")
        url = Logic.routeURL(routeQuery.get().id)
    else:
        print("3")
        defaultRoute = json.dumps(-1)
        url = Logic.routeURL(defaultRoute)
    markup = {
        "inline_keyboard" : [[{"text": "View Route", "url" : url},
                              {"text": "Finish", "callback_data" : "options"}]]
    }
    data["chat_id"] = target
    data["reply_markup"] = json.dumps(markup)
    data["message_id"] = message_id
    data["text"] = RESPONSES["VISUALISE"]
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/editMessageText",data=data
    )

def delete_message(chat_id, message_id):
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
    }
    ##################
    # DEBUGGING LINE #
    ##################
    # print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/deleteMessage",data=data
    )