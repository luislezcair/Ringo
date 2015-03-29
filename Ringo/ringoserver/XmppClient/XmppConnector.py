import logging
from django.conf import settings
from XmppClient import XmppClient
from Common.ServiceDiscoverer import ServiceDiscoverer


# Setup logging.
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s')

# Read settings
service_name = settings.RINGO['XMPP_SERVICE_NAME']

jid = "%s@%s" % (settings.RINGO['XMPP_USERNAME'], service_name)

password = settings.RINGO['XMPP_PASSWORD']

service = ServiceDiscoverer(service_name, settings.RINGO['XMPP_SERVICE_TYPE'])
service.discover()

address = (service.service_info['address'], service.service_info['port'])

room = "%s@%s.%s" % (service.service_info['txt']['muc_name'],
                     service.service_info['txt']['muc_host'],
                     service_name)

# Discover service address and port
logging.log(logging.INFO, address)

# Create xmpp client and connect to the server
xmpp = XmppClient(jid, password, room, nick='RingoServer')
xmpp.connect(address)
xmpp.process(block=False)
