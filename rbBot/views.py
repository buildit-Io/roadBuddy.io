from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Incoming
# hid keys in local _secrets.py NOT PUSHED TO GITHUB
from rb.settings._secrets import *
import json
import os
import requests

def index(request):
    return HttpResponse("Hello, world. This is the bot app.")

TELEGRAM_URL = "https://api.telegram.org/bot"
TOKEN = os.getenv("SECRET_KEY_2", SECRET_KEY_2)
# https://api.telegram.org/bot<token>/setWebhook?url=https://roadbuddy-io.herokuapp.com/rbBot/bot-hook/
class rbHookView(View):

    def post(self, request, *args, **kwargs):
        telegramData = json.loads(request.body)
        updateId = telegramData["update_id"]
        message = telegramData["message"]
        

        print(telegramData);
        x = Incoming(
            update_id = updateId,    
            message = message    
        )
        x.save();

        print(telegramData);

        msg = "roadBuddy.io is coming soon!"
        self.send_message(msg, message["chat"]["id"])
        return JsonResponse({"ok": "POST request processed"})
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TOKEN}/sendMessage", data=data
        )