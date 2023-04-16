from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .get_all_mails import get_all_emails
from .models import InfoCard
from .scripts.replace_https import short_url
from .scripts.get_favicon import *
from .scripts.avarage_color import *


@login_required
def profile_view(request):

    current_user = request.user
    user_id = current_user.id

    inf = InfoCard.objects.filter(user_id=user_id)

    return render(request, 'users/profile.html', {"inf": inf})


@login_required
def add_new_card(request):

    if request.method == 'POST':

        url = str(request.POST.get("url")).strip()

        infocard = InfoCard()
        infocard.url = url
        infocard.email = str(request.POST.get("email")).strip()
        infocard.password = str(request.POST.get("password")).strip()
        infocard.user_id = int(request.POST.get("user_id"))

        url_from_icon = short_url(url)
        infocard.name_of_service = url_from_icon

        try:
            infocard.icon = get_favicon_from_url(url_from_icon)
        except:
            return ""

        color_for_box_shadow = avarage_clr("fav.png")

        try:
            infocard.red = color_for_box_shadow[0]
            infocard.green = color_for_box_shadow[1]
            infocard.blue = color_for_box_shadow[2]
        except:
            return "Color error"

        try:
            infocard.save()
            return HttpResponseRedirect(reverse("profile"))
        except:
            return 'Error'

    return render(request, 'users/add_pass.html')


def reg_user(request):

    if request.method == "GET":

        return render(request, 'users/regform.html')

    else:

        username = str(request.POST.get("username")).strip()
        password = str(request.POST.get("password")).strip()
        password2 = str(request.POST.get("password2")).strip()
        email = str(request.POST.get("email")).strip()

        if len(username) < 4 or len(username) > 20:
            error = 'Логин должен быть > 4 и < 20 символов'
            return render(request, 'users/regform.html', {"error": error})
        elif password != password2:
            error = 'Пароли не совпадают'
            return render(request, 'users/regform.html', {"error": error})
        elif len(password) < 7 or len(password) > 25:
            error = 'Длина пароля должна быть больше 7 и меньше 25 символов'
            return render(request, 'users/regform.html', {"error": error})
        elif not '@' in email or not '.' in email or len(email.split('@')[0]) < 5:
            error = 'Неверный формат email'
            return render(request, 'users/regform.html', {"error": error})
        elif email in get_all_emails():
            error = 'Такой email уже существует'
            return render(request, 'users/regform.html', {"error": error})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect(reverse("home"))
        except:
            return 'Error'

        return render(request, 'users/regform.html')
