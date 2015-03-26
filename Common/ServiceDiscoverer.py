import dbus
import avahi
import gobject
import re
from dbus.mainloop.glib import DBusGMainLoop


DBusGMainLoop(set_as_default=True)


class ServiceNotFoundError(Exception):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return self.desc


class ServiceDiscoverer:
    def __init__(self, name, stype, timeout=5000):
        self.name = name
        self.stype = stype
        self.timeout = timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def onTimeout(self):
        self.loop.quit()
        raise ServiceNotFoundError('DNS service discovery timed out.')

    def discover(self, resolve_handler=None, error_handler=None):
        self.resolve_hanlder = resolve_handler
        self.error_handler = error_handler

        self.loop = gobject.MainLoop()
        bus = dbus.SystemBus()

        self.server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, '/'),
                                     'org.freedesktop.Avahi.Server')

        browser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
            self.server.ServiceBrowserNew(avahi.IF_UNSPEC, avahi.PROTO_INET,
                self.stype, 'local', dbus.Int32(0))),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER)

        browser.connect_to_signal('ItemNew', self.onServiceFound)

        gobject.timeout_add(self.timeout, self.onTimeout)
        self.loop.run()

    def onServiceFound(self, iface, proto, name, stype, domain, flags):
        if self.name not in name:
            return

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
        key_only = re.compile("(?P<key>.*)")
        txt_dict = {}

        for txt in txt_record:
            record = ''.join([chr(byte) for byte in txt])
            result = kvpair.match(record)
            if result:
                txt_dict[result.group('key')] = result.group('value')
            else:
                result = key_only.match(record)
                txt_dict[result.group('key')] = ''

        return txt_dict
