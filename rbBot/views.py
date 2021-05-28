from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. This is the bot app.")

def talkin_to_me_bruh(request):
    # please insert magic here
    return HttpResponse('OK')
