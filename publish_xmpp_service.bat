@echo off
cd %RINGO_PROJECT_PATH%
call env\Scripts\activate
python PublishXMPPBonjour.py