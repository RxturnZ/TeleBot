import os
import re
import time
import math
import heroku3
import requests
import time
from .. import StartTime
from heroku_config import Var
from userbot import telever
from userbot.uniborgConfig import Config
from datetime import datetime

Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Var.HEROKU_APP_NAME
HEROKU_API_KEY = Var.HEROKU_API_KEY

def check(tele):
    if "/start" in tele:
        return True
    wew = re.search(re.escape(f"\\b{tele}\\b"), "a|b|c|d")
    if wew:
        return True
    return False


# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "No Database is set"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION
    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "Functioning"
        is_database_working = True
    return is_database_working, output

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

async def telealive():
    _, check_sgnirts = check_data_base_heal_th()
    start = datetime.now()
    if Config.SUDO_USERS:
        sudo = "Enabled"
    else:
        sudo = "Disabled"
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    try:
        useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/80.0.3987.149 Mobile Safari/537.36'
                     )
        user_id = Heroku.account().id
        headers = {
            'User-Agent': useragent,
            'Authorization': f'Bearer {Config.HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        result = r.json()
        quota = result['account_quota']
        quota_used = result['quota_used']

        # Used
        remaining_quota = quota - quota_used
        math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)
        # Current
        App = result['apps']
        try:
            App[0]['quota_used']
        except IndexError:
            AppQuotaUsed = 0
        else:
            AppQuotaUsed = App[0]['quota_used'] / 60
            math.floor(App[0]['quota_used'] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)
        dyno = f"{AppHours}h {AppMinutes}m/{hours}h {minutes}m"
    except Exception as e:
        dyno = e
    conclusion = f"TeleBot Stats\
                  \n\nTeleBot Version : {telever}\
                  \nDatabase : {check_sgnirts}\
                  \nSudo : {sudo}\
                  \nUptime : {uptime}\
                  \nDyno : {dyno}\
                  "
    return conclusion
