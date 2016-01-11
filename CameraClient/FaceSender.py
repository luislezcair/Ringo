import sys
import requests
import json

#URL = "http://localhost:8000/doorbell/api/"
URL = "http://192.168.1.105:8000/doorbell/api/"
PICTURE_URL = URL + "pictures/"
RECT_URL = URL + "rects/"

USER = 'doorbell'
PASSWORD = 'doorbell-123'
AUTH = (USER, PASSWORD)


class FaceSender:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = AUTH

    def post_picture(self, image, fmt):
        files = {'picture': ('jondoe.%s' % fmt, image, 'image/%s' % fmt)}
        response = self.session.post(PICTURE_URL, files=files)

        response.raise_for_status()

        j = response.json()
        return j['url']

    def post_rect(self, rects):
        headers = {'Content-Type': 'application/json'}
        response = self.session.post(RECT_URL,
                                     data=json.dumps(rects),
                                     headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            with open("debug.html", "w") as f:
                f.write(e.response.text)

    def close(self):
        self.session.close()

    @staticmethod
    def on_error(args):
        print("Error: %s" % args)
        sys.exit(1)
