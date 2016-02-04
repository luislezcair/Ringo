from django.conf import settings
from ringoserver.xmpp import xmppclient as xmpp

# Read settings
jid = "%s@%s" % (settings.RINGO['XMPP_USERNAME'], settings.RINGO['XMPP_SERVICE_NAME'])
password = settings.RINGO['XMPP_PASSWORD']
address = (settings.RINGO['XMPP_SERVER'], settings.RINGO['XMPP_SERVER_PORT'])
room = "%s@%s.%s" % (settings.RINGO['XMPP_MUC_NAME'],
                     settings.RINGO['XMPP_MUC_HOST'],
                     settings.RINGO['XMPP_SERVICE_NAME'])


def connect_and_send(json):
    client = xmpp.XMPPClient(jid=jid,
                             password=password,
                             room=room,
                             nick='TheDoorbell')

    client.connect(address=address)
    client.process(block=False)
    client.disconnect_after_send = True
    client.send_muc_message(json)
