@echo off
cd %RINGO_PROJECT_PATH%
call env\Scripts\activate
cd Ringo
python manage.py ejabberd_auth