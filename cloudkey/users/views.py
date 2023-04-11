from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .get_all_mails import get_all_emails


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


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
