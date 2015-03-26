import logging
from django.conf import settings
from XmppClient import XmppClient
from Common.ServiceDiscoverer import ServiceDiscoverer


# Setup logging.
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s')

# Read settings
jid = "%s@%s" % (settings.RINGO['XMPP_USERNAME'],
                 settings.RINGO['XMPP_SERVICE_NAME'])

password = settings.RINGO['XMPP_PASSWORD']
nick = settings.RINGO['XMPP_MUC_NICKNAME']

room = "%s@%s.%s" % (settings.RINGO['XMPP_MUC_NAME'],
                     settings.RINGO['XMPP_MUC_HOST'],
                     settings.RINGO['XMPP_SERVICE_NAME'])

# Discover service address and port
service = ServiceDiscoverer(settings.RINGO['XMPP_SERVICE_NAME'],
                            settings.RINGO['XMPP_SERVICE_TYPE'])
service.discover()

address = (service.service_info['address'],
           service.service_info['port'])

logging.log(logging.INFO, address)

# Create xmpp client and connect to the server
xmpp = XmppClient(jid, password, room, nick)
xmpp.connect(address)
xmpp.process(block=False)
