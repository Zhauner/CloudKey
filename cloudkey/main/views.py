from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def bot_info(request):
    return render(request, 'main/telbot.html')
