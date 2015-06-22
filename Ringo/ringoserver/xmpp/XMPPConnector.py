import logging
from django.conf import settings
from ServiceDiscoverer import ServiceDiscoverer


# Setup logging.
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s')
#                     # filename='/home/ringo/debug.log')

connection_info = {}

# Read settings
service_name = settings.RINGO['XMPP_SERVICE_NAME']

connection_info['jid'] = "%s@%s" % (settings.RINGO['XMPP_USERNAME'], service_name)

connection_info['password'] = settings.RINGO['XMPP_PASSWORD']

service = ServiceDiscoverer(service_name, settings.RINGO['XMPP_SERVICE_TYPE'])
service.discover()

connection_info['address'] = (service.service_info['address'], service.service_info['port'])

connection_info['room'] = "%s@%s.%s" % (service.service_info['txt']['muc_name'],
                                        service.service_info['txt']['muc_host'],
                                        service_name)

# Discover service address and port
logging.log(logging.INFO, connection_info['address'])
