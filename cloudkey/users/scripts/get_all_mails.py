import sqlite3


def get_all_emails():

    all_emails = []

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()

    result = cursor.execute("SELECT email FROM auth_user")

    for x in result.fetchall():
        all_emails.append(*x)

    return all_emails


def get_all_nicknames():

    all_nicknames = []

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()

    result = cursor.execute("SELECT username FROM auth_user")

    for x in result.fetchall():
        all_nicknames.append(*x)

    return all_nicknames
