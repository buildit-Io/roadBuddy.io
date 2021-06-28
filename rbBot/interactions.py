import os
from .speech import RESPONSES, REPLY_MATRIX, MARKUP_MATRIX, CALLBACK_MATRIX
import requests
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

def welcome(target,user):
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

def planCallback(target):
    return answer_callback("DEFAULT",RESPONSES["PLAN_CALLBACK"],target)

def editCallback(target):
    return answer_callback("DEFAULT",RESPONSES["EDIT_CALLBACK"],target)

def notplanCallback(target):
    return answer_callback("DEFAULT",RESPONSES["NOTPLAN_CALLBACK"],target)

def backCallback(target):
    return answer_callback("DEFAULT",RESPONSES["BACK_CALLBACK"],target)

def preRoutingCallback(target):
    return answer_callback("DEFAULT",RESPONSES["WARNING_CALLBACK"],target)

def preQuitCallback(target):
    return answer_callback("DEFAULT",RESPONSES["WARNING_CALLBACK"],target)

def quitCallback(target):
    return answer_callback("DEFAULT",RESPONSES["QUIT_CALLBACK"],target)

def invalidCallback(target):
    return answer_callback("INVALID",RESPONSES["INVALID_CALLBACK"],target)

def routeCallback(target):
    return answer_callback("VISUALISE",RESPONSES["VISUALISE_CALLBACK"],target)

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

def addDest(target,message_id):
    return edit_message("PLAN",RESPONSES["PLAN"],target,message_id)

def editPlan(target,message_id):
    return edit_message("EDIT_PLAN",RESPONSES["EDIT_PLAN"],target,message_id)

def notplanClicked(target,message_id):
    return edit_message("NOTPLAN",RESPONSES["NOTPLAN"],target,message_id)

def backToOptions(target,message_id):
    return edit_message("BACK_TO_OPTIONS",RESPONSES["OPTIONS"],target,message_id)

def preRouting(target,message_id):
    return edit_message("PLAN_NEXT",RESPONSES["PLAN_NEXT"],target,message_id)

def route(target,message_id):
    return edit_message("BACK_TO_OPTIONS",RESPONSES["OPTIONS"],target,message_id)

def preQuit(target,message_id):
    return edit_message("PRE_QUIT",RESPONSES["PRE_QUIT"],target,message_id)

def inlineQuit(target,message_id,user):
    return edit_message("QUIT",RESPONSES["QUIT"](user.first_name,user.last_name),target,message_id)

def commandQuit(target,user):
    return send_message("QUIT",RESPONSES["QUIT"](user.first_name,user.last_name),target)
