import json
import requests
import rbBot.botbrain.logic as Logic

def welcome(firstName, lastName):
    if lastName == "null":
        text = "Welcome back, {name}!".format(name=firstName)
    else:
        text = "Welcome back, {first_name} {last_name}!".format(first_name=firstName,last_name=lastName)
    return text

def quit(firstName, lastName):
    if lastName == "null":
        text = "See you again, {name}!".format(name=firstName)
    else:
        text = "See you again, {first_name} {last_name}!".format(first_name=firstName,last_name=lastName)
    return text

def resumePlan(dests):

    return ("<strong><i>Send</i></strong> the postal addresses/addresses of each destination <strong><i>as a message</i></strong> to the bot." + 
              "\n\n<strong>Invalid addresses will be flagged out</strong>" +
              "\n\nLogged destinations:\n" + 
              ''.join(['\n%s - %s' % kv for kv in dests.items()]))

def invalidPlan(dests):

    return ("<strong><i>Less than 2 destinations detected. Please key in at least 2 destinations.</i></strong>" + 
              "\n\n<strong>Invalid addresses will be flagged out to you</strong>" +
              "\n\nYour currently logged destination(s):" + 
              ''.join(['\n%s - %s' % kv for kv in dests.items()]))

def addDest(dests):
    return ("<strong><i>The destination is valid and has been added to the route plan!</i></strong>" + 
            "\n\nLogged destinations:\n" + 
            ''.join(['\n%s - %s' % kv for kv in dests.items()]) + 
            "\n\n<strong><i>Send</i></strong> the postal addresses/addresses of each destination <strong><i>as a message</i></strong> to the bot.")
    
def edit(dests):
    return ("<strong><i>Please choose how you want to amend your plan</i></strong>" +
            "\n\nPress <i>Done</i> once you are satisfied with the changes" +
            "\n\nYour destinations:" + 
            ''.join(['\n%s - %s' % kv for kv in dests.items()]) )

def reflectValid(oldLoc,newLoc):
   return (f"The address <strong><i>{newLoc}</i></strong> is valid and can be used to replace <strong><i>{oldLoc}</i></strong>!")

def reflectInvalid(dests):
    if type(dests) == dict:
        return ("<strong><i>The address entered cannot be found. Postal Codes work best!</i></strong>" +
                  "\n\nLogged destinations:\n" + 
                  ''.join(['\n%s - %s' % kv for kv in dests.items()]) +
                  "\n\n<strong><i>Send</i></strong> the postal addresses or addresses of your destinations <strong><i> as a message</i></strong> to the bot.")
    if type(dests) == list:
        new = dests[1]
        old = dests[0]
        return (f"The address <strong><i>{new}</i></strong> cannot be found. \n\nDestination to change: <strong><i>{old}</i></strong>")

def confirmDest(dests):
    return ("<strong><i>Please ensure that ALL destinations have been added before generating the route</i></strong>" +
              "\n\nLogged destinations:\n" +
              ''.join(['\n%s - %s' % kv for kv in dests.items()]) + 
              "\n\nPress <i>Back</i> to continue adding destinations" )

def routeDetails(dests):
    return "Route Details:\n" + ''.join(['\n%s - %s' % kv for kv in dests.items()])

RESPONSES = {
    "DEFAULT" : "Please input a valid command",
    "REGISTER_QUERY" : "System does not recognise you. Do you want to register?",
    "REGISTERED" : "You have been added to the database and can now use the bot!",
    "NEXT_TIME" : "Alright Maybe Next Time!",
    "WELCOME" : welcome,
    "OPTIONS" : "What would you like to do?",
    "PLAN" : ("<strong><i>Send</i></strong> the postal addresses/addresses of each destination<strong><i> as a message</i></strong> to the bot." + 
              "\n\n<strong>Invalid addresses will be flagged out</strong>" +
              "\n\n<strong>A minimum of 2 destinations must be entered</strong>" +
              "\n\nYour current session will be saved."),
    "INVALID_PLAN" : invalidPlan,
    "INVALID_EDIT_PLAN" : "<strong><i>No destinations detected. Please key in at least 1 destination.</i></strong>",
    "NO_REPLACEMENT" : "Please key in a replacement destination",
    "PRE_PLAN" : ("<strong>You have a saved session.</strong>" +
                    "\n\n<strong>Start New</strong> - <i>Restart route planning</i>" +
                    "\n<strong>Resume</strong> - <i>Continue previous route planning</i>" +
                    "\n<strong>Back</strong> - <i>Choose other options</i>" +
                    "\n\n<strong>Press <i>Back</i> to choose other options</strong>"),
    "PRE_RESET" : ("<strong>Warning: Your current route will not be saved</strong>"),
    "PRE_WIPE" : ("<strong>Warning: All previouosly saved routes will be destroyed</strong>"),
    "RESUME_PLAN" : resumePlan,
    "ADD" : addDest,
    "INVALID_DEST" : reflectInvalid,
    "VALID_DEST" : reflectValid,
    "NOTPLAN" : ("<b>Saved Routes</b> - <i>View all the routes logged with roadBuddy</i>" + 
                 "\n\n<b>Wipe Data</b> - <i>Delete all the data related to you on the Server</i>" + 
                 "\n\n<b>Back</b> - <i>Go Back to the previous menu</i>"),
    "PLAN_NEXT" : confirmDest,
    "EDIT" : edit,
    "EDIT_DESTS" : "Choose the destination to change",
    "CHANGE_DEST" : "Key in the new destination",
    "GET_SAVED" : "View and choose your saved routes here",
    "ROUTE_DETAILS" : routeDetails,
    "CHANGE_DEST_NEXT" : "<strong>Warning: You are changing the current destination</strong>",
    "VISUALISE" : "<strong>Your Route has been generated!</strong>",
    "PRE_QUIT" : ("You are about to quit the session." +
                  "\n\n<strong><i>All progress will Be LOST</i></strong>" +
                   "\n\nAre you sure you want to <i>proceed</i>?"),
    "QUIT" : quit,
    "PLAN_CALLBACK" : "Send the postal code/address as a message",
    "INVALID_PLAN_CALLBACK" : "Missing minimum number of destinations",
    "NOTPLAN_CALLBACK" : "Choose other functionality",
    "GET_SAVED_CALLBACK" : "Your routes",
    "ROUTE_DETAILS_CALLBACK" : "Selected Route Details",
    "BACK_CALLBACK" : "Back to Previous Menu",
    "WARNING_CALLBACK" : "Before Continuing...",
    "EDIT_CALLBACK" : "Make changes to your plan",
    "EDIT_DESTS_CALLBACK" : "Choose the destination to change",
    "CHANGE_DEST_CALLBACK" : "Send the new destination",
    "CONFIRM_CHANGE_DEST_CALLBACK" : "Destination has been changed",
    "QUIT_CALLBACK" : "We hope you had a pleasant experience!",
    "INVALID_CALLBACK" : "This message has expired and is no longer valid",
    "RESET_CALLBACK" : "Your saved route has been deleted",
    "WIPE_CALLBACK" : "Your data has been cleared",
    "VISUALISE_CALLBACK" : "Generating Route...",
    "NA_CALLBACK" : "This function isn't available yet",
    "PLAN_HELP_CALLBACK" : ("Continue: Proceed to generate Route" +
              "\nEdit Plan: Edit the current entries" +
              "\nBack: Choose other options" +
              "\nHelp: View what each button does"),
}

MARKUP_MATRIX = {
    "REGISTER" : {
        "keyboard" : [[{"text": "Register"}],[{"text": "Back"}]], 
        "resize_keyboard" : True, 
        "one_time_keyboard": True,
    },
    "OPTIONS" : {
        "inline_keyboard" : [[{"text": "Plan a journey", "callback_data" : "plan"}],
                             [{"text": "Others", "callback_data" : "not_plan"}],
                             [{"text": "Quit", "callback_data" : "pre_quit"}]
                             ]
    },
    "REMOVE_KEYBOARD" : {
        "remove_keyboard" : True,  
    },
    "PRE_PLAN" : {
        "inline_keyboard" : [[{"text": "Start New", "callback_data" : "reset_plan"}],
                             [{"text": "Resume", "callback_data" : "resume_plan"}],
                             [{"text": "Back", "callback_data" : "options"}]
                             ]  
    },
    "PRE_RESET" : {
        "inline_keyboard" : [[{"text": "Yes, start a new session", "callback_data" : "reset_plan_clicked"}],
                             [{"text": "Back", "callback_data" : "pre_plan"}]
                             ]  
    },
    "PLAN" : {
        "inline_keyboard" : [[{"text": "Continue", "callback_data" : "plan_next"},{"text": "Edit Plan", "callback_data" : "edit"}],
                             [{"text": "Back", "callback_data" : "options"},{"text": "Help", "callback_data" : "plan_help"}],
                             ]  
    },
    "NOTPLAN" : {
        "inline_keyboard" : [[{"text": "Saved Routes", "callback_data" : "get_saved"}],
                             [{"text": "Wipe Data", "callback_data" : "pre_wipe"}],
                             [{"text": "Settings", "url" : Logic.settingsURL()}],
                             [{"text": "Back", "callback_data" : "options"}]
                             ]  
    },
    "PLAN_NEXT" : {
        "inline_keyboard" : [[{"text": "Generate Route", "callback_data" : "visualise"}],
                             [{"text": "Back", "callback_data" : "plan"}],
                             ]
    },
    "CHANGE_DEST" : {
        "inline_keyboard" : [[{"text": "Proceed", "callback_data" : "change_dest_next"}],
                             [{"text": "Back", "callback_data" : "edit_dests"}],
                             ]
    },
    "CHANGE_DEST_NEXT" : {
        "inline_keyboard" : [[{"text": "Confirm Change", "callback_data" : "confirm_change_dest"}],
                             [{"text": "Back", "callback_data" : "change_dest"}],
                             ]
    },
    "PRE_QUIT" : {
        "inline_keyboard" : [[{"text": "Yes, I want to quit", "callback_data" : "quit"}],
                             [{"text": "Back", "callback_data" : "options"}],
                             ]
    },
    "PRE_WIPE" : {
        "inline_keyboard" : [[{"text": "Yes, I want to wipe all data.", "callback_data" : "wipe"}],
                             [{"text": "Back", "callback_data" : "not_plan"}],
                             ]
    },
}

REPLY_MATRIX = {
    "DEFAULT" : {
        "chat_id": "",
        "text": "",
        "parse_mode": "Markdown",
    },
    "REGISTER_QUERY" : {
        "chat_id": "",
        "text": "",
        "reply_markup": json.dumps(MARKUP_MATRIX['REGISTER']),
    },
    "OPTIONS" : {
        "chat_id": "",
        "text": "",
        "reply_markup": json.dumps(MARKUP_MATRIX['OPTIONS']),
    }, 
    "PRE_PLAN" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PRE_PLAN']),
    },  
    "PRE_RESET" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PRE_RESET']),
    },  
    "PLAN" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PLAN']),
    },  
    "NOTPLAN" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['NOTPLAN']),
    }, 
    "BACK_TO_OPTIONS" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['OPTIONS']),
    },   
    "PLAN_NEXT" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PLAN_NEXT']),
    },     
    "CHANGE_DEST" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['CHANGE_DEST']),
    },    
    "CHANGE_DEST_NEXT" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['CHANGE_DEST_NEXT']),
    },    
    "URL" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": "",
    }, 
    "PRE_QUIT" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PRE_QUIT']),
    },  
    "PRE_WIPE" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PRE_WIPE']),
    }, 
    "QUIT" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html"
    }, 
    "REMOVE_KEYBOARD" : {
        "chat_id": "",
        "text": "",
        "reply_markup": json.dumps(MARKUP_MATRIX['REMOVE_KEYBOARD']),
    },
}

CALLBACK_MATRIX = {
    "DEFAULT" : {
        "callback_query_id": "",
        "text": "",
        "show_alert": False,
        "url": "",
        "cache_time": 0,
    },
    "INVALID" : {
        "callback_query_id": "",
        "text": "",
        "show_alert": True,
        "url": "",
        "cache_time": 0,
    }
}