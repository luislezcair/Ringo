Ringo Smart Doorbell
===================

Ringo is a project aimed to build a smart doorbell wich can recognize the people 
standing in the door. It will notify the residents of a house directly in their
smartphones with audio and video.

The project is still in very early stages of development.

#### Directory structure
- `CameraClient`: Utility to take pictures, detect faces and send them to the web server via a REST API.
- `Util`: Utilities to train the detector and detect and recognize faces.
- `Ringo`: Directory containing the web project along with three apps:
	- `ringoserver`: Web app that receives a face and posts it in a multiuser chat room of a XMPP server.
	- `webadmin`: Web app for managing Ringo settings.
	- `ejabberd_auth`: App used by ejabberd to authenticate users against Django.

#### ejabberd configuration
ejabberd is used to broadcast notifications to all devices connected to the chat room defined here. When a visitor arrives, we take a picture, process it and send it to ejabberd where the devices are listening, along with the recognized visitor (if any).

The devices can find the XMPP server in the local network thanks to DNS Service Discovery (DNS-SD). For this, we use Avahi in Linux and Apple's Bonjour in Windows. There has to be a service properly configured with the same settings as ejabberd.

Here is a brief step-by-step guide of which settings are necessary:

 - Install ejabberd.
 - Create a virtualhost called "RingoXMPPServer".
 - Use external authentication with the script provided in the repository.
 - Create a multiuser chat room "Ringo" and make it persistent.
 - Generate self-signed certificate for the vhost.
 - Configure Avahi/Bonjour with ejabberd configuration:
	- Service type: "_xmpp-server._tcp".
	- Port: 5222.
	- Service name: RingoXMPPServer.
	- TXT record: muc_host=conference, muc_name=ringo.

 - Set an eviroment var called `RINGO_PROJECT_PATH` that points to the project directory.
 - Add "ringoxmppserver" to the hosts file with a LAN IP address.
