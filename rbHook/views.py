import json
import os

import requests
from django.http import JsonResponse
from django.views import View

from .models import incoming

os.environ['SECRET_TOKEN'] = "1762553405:AAGTA9OGDw5KKZfEDcimysIx09-uud5QEOA";

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = os.getenv("SECRET_TOKEN", "error_token")


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhook/
class rbHookView(View):

    def post(self, request, *args, **kwargs):
        telegramData = json.loads(request.body)
        updateId = telegramData["update_id"]
        message = telegramData["message"]
    
        x = incoming(
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
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )