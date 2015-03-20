import cv2
import struct
import requests
import json
from ServiceDiscoverer import ServiceDiscoverer


ringo_ip = ''
ringo_port = 0

def on_service_resolved(sinfo):
    global ringo_ip, ringo_port
    ringo_ip = sinfo['address']
    ringo_port = sinfo['port']

def on_resolve_error(error):
    print(error)

service = ServiceDiscoverer("RingoHTTPMediaServer", "_http._tcp")
service.discover(on_service_resolved, on_resolve_error)

print(ringo_ip)
print(ringo_port)

opencv_data_dir = '/usr/share/OpenCV'

faceCascade = cv2.CascadeClassifier(opencv_data_dir + '/haarcascades/haarcascade_frontalface_alt_tree.xml')
capture = cv2.VideoCapture(-1)

while True:
    retVal, frame = capture.read()
    
    key = cv2.waitKey(1)
    if key == 13:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(grayFrame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)

        if faces != ():
            cv2.imshow('Face', frame)
            retVal, image = cv2.imencode('.png', frame)
            s = ""
            for i in image:
                s += struct.pack('B', i[0])

            ringo_server = 'http://%s:%s' % (ringo_ip, ringo_port)

            auth = ('ringo', 'ringo-123')
            files = {'picture': ('jondoe.png', s, 'image/png')}

            picture_endpoint = '%s/pictures/' % ringo_server
            rect_endpoint = '%s/rects/' % ringo_server

            r = requests.post(picture_endpoint, auth=auth, files=files)

            j = r.json()
            picture_url = j['url']

            headers = {'Content-Type': 'application/json'}

            payload = []
            for (x, y, w, h) in faces:
                payload.append({'x': str(x), 'y': str(y),
                                'width': str(w), 'height': str(h),
                                'picture': picture_url})
            
            r = requests.post(rect_endpoint,
                              auth=auth,
                              data=json.dumps(payload),
                              headers=headers)

#            f = open('debug.html', 'w')
#            f.write(r.text)
#            f.close()
         
    elif key == 27:
        break
    
    cv2.imshow('Ringo Capture', frame)
