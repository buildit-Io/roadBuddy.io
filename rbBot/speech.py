import json

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

RESPONSES = {
    "DEFAULT" : "Please input a valid command",
    "REGISTER_QUERY" : "System does not recognise you. Do you want to register?",
    "REGISTERED" : "You have been added to the database and can now use the bot!",
    "NEXT_TIME" : "Alright Maybe Next Time!",
    "WELCOME" : welcome,
    "OPTIONS" : "What would you like to do?",
    "PLAN" : ("<strong><i>Send</i></strong> the postal addresses or addresses of your destinations <strong><i>as a message</i></strong> to the bot." + 
              "\n\n<strong>Invalid Inputs will be filtered out</strong>" +
              "\n\nYour destinations:"),
    "NOTPLAN" : ("<b>Saved Routes</b> - <i>View all the routes logged with roadBuddy</i>" + 
                 "\n\n<b>Wipe Data</b> - <i>Delete all the data related to you on the Bot Server</i>" + 
                 "\n\n<b>Back</b> - <i>Go Back to the previous menu</i>"),
    "PLAN_NEXT" : ("<strong><i>Please ensure that ALL destinations have been added before generating the route</i></strong>" +
                   "\n\nPress <i>Back</i> to continue adding destinations" +
              "\n\nYour destinations:"),
    "EDIT_PLAN" : ("<strong><i>Please choose the destination you want to amend</i></strong>" +
                   "\n\nPress <i>Done</i> once you are satisfied with the changes" +
              "\n\nYour destinations:"),
    "PRE_QUIT" : ("You are about to quit the session." +
                  "\n\n<strong><i>All progress will Be LOST</i></strong>" +
                   "\n\nAre you sure you want to <i>proceed</i>?"),
    "QUIT" : quit,
    "PLAN_CALLBACK" : "Send the postal code/address as a message",
    "NOTPLAN_CALLBACK" : "Choose other functionality",
    "BACK_CALLBACK" : "Back to Previous Menu",
    "WARNING_CALLBACK" : "Before Continuing...",
    "EDIT_CALLBACK" : "Make changes to your plan!",
    "QUIT_CALLBACK" : "We hope you had a pleasant experience!",
    "INVALID_CALLBACK" : "This message has expired and is no longer valid.",
    "VISUALISE_CALLBACK" : "Generating Route...",
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
    "PLAN" : {
        "inline_keyboard" : [[{"text": "Continue", "callback_data" : "plan_next"}],
                             [{"text": "Edit Plan", "callback_data" : "edit_plan"}],
                             [{"text": "Back", "callback_data" : "options"}]
                             ]  
    },
    "NOTPLAN" : {
        "inline_keyboard" : [[{"text": "Saved Routes", "callback_data" : "get_saved"}],
                             [{"text": "Wipe Data", "callback_data" : "wipe"}],
                             [{"text": "Back", "callback_data" : "options"}]
                             ]  
    },
    "PLAN_NEXT" : {
        "inline_keyboard" : [[{"text": "Generate Route", "callback_data" : "visualise"}],
                             [{"text": "Back", "callback_data" : "plan"}],
                             ]
    },
    "EDIT_PLAN" : {
        "inline_keyboard" : [[{"text": "Done", "callback_data" : "plan"}],
                             ]
    },
    "PRE_QUIT" : {
        "inline_keyboard" : [[{"text": "Yes, I want to quit", "callback_data" : "quit"}],
                             [{"text": "Back", "callback_data" : "options"}],
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
    "EDIT_PLAN" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['EDIT_PLAN']),
    }, 
    "PRE_QUIT" : {
        "chat_id": "",
        "message_id": "",
        "inline_message_id": "",
        "text": "",
        "parse_mode" : "Html",
        "reply_markup": json.dumps(MARKUP_MATRIX['PRE_QUIT']),
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
    },
    "VISUALISE" : {
        "chat_id": "",
        "text": "",
        "show_alert": False,
        "url": "www.google.com",
        "cache_time": 0,
    },
}