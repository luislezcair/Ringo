import sys
import requests
import json
from Common.ServiceDiscoverer import ServiceDiscoverer, ServiceNotFoundError

class FaceSender:
    def __init__(self):
        self.session = requests.Session()

    def get_service_info(self, name):
        sd = ServiceDiscoverer(name, "_http._tcp")
        sd.discover(error_handler=self.on_error)

        url = 'http://%s:%s%s' %  (sd.service_info['address'],
                                   sd.service_info['port'],
                                   sd.service_info['txt']['doorbell_api'])

        self.picture_endpoint = url + 'pictures/'
        self.rect_endpoint = url + 'rects/'

    def set_auth(self, user, password):
        self.session.auth = (user, password)

    def post_picture(self, image, fmt):
        files = {'picture': ('jondoe.%s' % fmt, image, 'image/%s' % fmt)}
        response = self.session.post(self.picture_endpoint, files=files)

        response.raise_for_status()

        j = response.json()
        return j['url']

    def post_rect(self, rects):
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(self.rect_endpoint, 
                                     data=json.dumps(rects),
                                     headers=headers)
        response.raise_for_status()

    def close(self):
        self.session.close()

    def on_error(self, args):
        print("Error: %s" % args)
        sys.exit(1)
