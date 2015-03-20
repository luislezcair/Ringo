from threading import Thread
from django.conf import settings
from XmppClient import XmppClient
from ServiceDiscoverer import ServiceDiscoverer
import logging


class XmppConnector:
    def __init__(self):
        sname = settings.RINGO['XMPP_SERVICE_NAME']
        stype = settings.RINGO['XMPP_SERVICE_TYPE']

        self.avahi = ServiceDiscoverer(sname, stype)

    def discover(self):
        self.avahi.discover(self.service_resolved, self.resolve_error)

    def service_resolved(self, service_info):
        self.address = (service_info['address'], service_info['port'])

    def resolve_error(self, error):
        print(error)


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
connector = XmppConnector()
connector.discover()

logging.log(logging.INFO, connector.address)

# Create xmpp client and connect to the server
xmpp = XmppClient(jid, password, room, nick)
xmpp.connect(connector.address)
xmpp.process(block=False)

