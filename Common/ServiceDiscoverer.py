import dbus
import avahi
import gobject
import re
from dbus.mainloop.glib import DBusGMainLoop


DBusGMainLoop(set_as_default=True)


class ServiceDiscoverer:
    def __init__(self, name, stype):
        self.name = name
        self.stype = stype
        self.loop = gobject.MainLoop()

    def discover(self, resolve_handler=None, error_handler=None):
        self.resolve_hanlder = resolve_handler
        self.error_handler = error_handler

        bus = dbus.SystemBus()

        self.server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, '/'),
                                     'org.freedesktop.Avahi.Server')

        browser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
            self.server.ServiceBrowserNew(avahi.IF_UNSPEC, avahi.PROTO_INET,
                self.stype, 'local', dbus.Int32(0))),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER)

        browser.connect_to_signal('ItemNew', self.onServiceFound)

        self.loop.run()

    def onServiceFound(self, iface, proto, name, stype, domain, flags):
        self.server.ResolveService(iface, proto, name, stype, domain,
                avahi.PROTO_UNSPEC, dbus.UInt32(0),
                reply_handler=self.onServiceResolved,
                error_handler=self.onServiceResolveError)

    def onServiceResolved(self, *args):
        self.loop.quit()

        txt_record = self.parse_txt(args[9])

        self.service_info = {'protocol': int(args[1]),
                             'service_name': str(args[2]),
                             'address': str(args[7]),
                             'port': int(args[8]),
                             'txt': txt_record}

        if self.resolve_hanlder:
            self.resolve_hanlder(self.service_info)

    def onServiceResolveError(self, args):
        self.loop.quit()
        if self.error_handler:
            self.error_handler(args)

    def parse_txt(self, txt_record):
        kvpair = re.compile("(?P<key>.*)=(?P<value>.*)")
        txt_dict = {}

        for txt in txt_record:
            record = ''.join([chr(byte) for byte in txt])
            r = kvpair.match(record)
            txt_dict[r.group('key')] = r.group('value')

        return txt_dict
