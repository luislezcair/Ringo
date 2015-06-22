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
        self.timeout_id = None

    def set_timeout(self, timeout):
        self.timeout = timeout

    def on_timeout(self):
        self.loop.quit()

        if self.error_handler:
            e = ServiceNotFoundError("DNS service discovery timed out. "
                                     "Service %s not found" % self.name)
            self.error_handler(e)

        return False

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

        browser.connect_to_signal('ItemNew', self.on_service_found)

        self.timeout_id = gobject.timeout_add(self.timeout, self.on_timeout)
        self.loop.run()

    def on_service_found(self, iface, proto, name, stype, domain, flags):
        if self.name not in name:
            return

        self.server.ResolveService(iface, proto, name, stype, domain,
                                   avahi.PROTO_INET, dbus.UInt32(0),
                                   reply_handler=self.on_service_resolved,
                                   error_handler=self.on_service_resolve_error)

    def on_service_resolved(self, *args):
        gobject.source_remove(self.timeout_id)
        self.loop.quit()

        txt_record = self.parse_txt(args[9])

        self.service_info = {'protocol': int(args[1]),
                             'service_name': str(args[2]),
                             'address': str(args[7]),
                             'port': int(args[8]),
                             'txt': txt_record}

        if self.resolve_hanlder:
            self.resolve_hanlder(self.service_info)

    def on_service_resolve_error(self, args):
        gobject.source_remove(self.timeout_id)
        self.loop.quit()

        if self.error_handler:
            self.error_handler(args)

    @staticmethod
    def parse_txt(txt_record):
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
