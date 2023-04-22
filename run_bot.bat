@echo off

call %~dp0venv\Scripts\activate

cd %~dp0cloudkey_bot

set TOKEN=5858206164:AAE_N29MnhUKjc_Xox2sxRP8ogVJJ6Snp7k

python bot.py

pause