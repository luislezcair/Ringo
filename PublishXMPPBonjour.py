import select
import pybonjour


SERVICE_NAME = 'RingoXMPPServer'
SERVICE_TYPE = '_xmpp-server._tcp'
SERVICE_PORT = 5222
XMPP_MUC_NAME = 'Ringo'
XMPP_MUC_HOST = 'conference'
TXTRECORD = pybonjour.TXTRecord({'muc_name': XMPP_MUC_NAME, 'muc_host': XMPP_MUC_HOST})


def register_callback(ref, flags, error_code, name, regtype, domain):
    if error_code == pybonjour.kDNSServiceErr_NoError:
        print 'Ringo service registered:'
        print '  name    =', name
        print '  regtype =', regtype
        print '  domain  =', domain

serviceRef = pybonjour.DNSServiceRegister(name=SERVICE_NAME,
                                          regtype=SERVICE_TYPE,
                                          port=SERVICE_PORT,
                                          txtRecord=TXTRECORD,
                                          callBack=register_callback)

try:
    while True:
        ready = select.select([serviceRef], [], [], 10)
        if serviceRef in ready[0]:
            pybonjour.DNSServiceProcessResult(serviceRef)
except KeyboardInterrupt:
    print("Finishing...")
finally:
    serviceRef.close()
