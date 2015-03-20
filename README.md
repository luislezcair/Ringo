Ringo Smart Doorbell
===================

Ringo is a project aimed to build a smart doorbell wich can recognize the people standing in the door. It will notify the residents of a house directly in their smartphones with a 
audio and video.

#### Directory structure
- `camera`: Utility to take pictures, detect faces and send them to the web server via the REST API.
- `RingoApp`: Andorid app that receives the notifications from the server.
- `Ringo`: Directory containing the web project along with three apps:
	- `ringoserver`: Web app that receives a face and posts it in a multiuser chat room of a XMPP server.
	- `webadmin`: Web app for managing Ringo settings.
	- `ejabberd_auth`: App used by ejabberd to authenticate users against Django.
