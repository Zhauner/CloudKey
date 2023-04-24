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
            return False
        elif user == []:

            cursor.execute(f'SELECT * FROM auth_user WHERE email = "{login}";')
            user = cursor.fetchall()

            if user != [] and check_password(password, user[0][1]):
                return user[0][0]
            else:
                return False
        connect.close()

    def show_datas_by_id(self, user_id):
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(f'SELECT * FROM users_infocard WHERE user_id = "{user_id}";')
        return cursor.fetchall()

#
# ddd = SQLiteConnect('C:\\Users\\Stas\\Desktop\\CloudKey\\cloudkey\\db.sqlite3')
#
# print(ddd.show_datas_by_id(1))