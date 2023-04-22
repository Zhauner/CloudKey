import sqlite3
from django.conf import settings
from django.contrib.auth.hashers import check_password

settings.configure()


class SQLiteConnect:

    def __init__(self, path: str):
        self.path = path

    def pass_and_login_check(self, login, password):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(f'SELECT * FROM auth_user WHERE username = "{login}";')
        user = cursor.fetchall()

        if user != [] and check_password(password, user[0][1]):

            return user[0][0]

        elif user != [] and not check_password(password, user[0][1]):
            return 'Неверный login(email) или пароль'
        elif user == []:

            cursor.execute(f'SELECT * FROM auth_user WHERE email = "{login}";')
            user = cursor.fetchall()

            if user != [] and check_password(password, user[0][1]):
                return user[0][0]
            else:
                return 'Неверный login(email) или пароль'
