import cv2
import numpy
import struct
from FaceSender import FaceSender


cascade_dir = '/usr/share/opencv/haarcascades/'

cascade_files = ['haarcascade_frontalface_alt_tree.xml',
                 'haarcascade_frontalface_alt.xml',
                 'haarcascade_frontalface_alt2.xml',
                 'haarcascade_frontalface_default.xml',
                 'haarcascade_profileface.xml']

cascades = [cv2.CascadeClassifier(cascade_dir + c) for c in cascade_files]


def detect_face(frame):
    for c in cascades:
        faces = c.detectMultiScale(frame, minSize=(40, 40))
        if len(faces) > 0:
            return faces
    return numpy.empty(0)


def frame_to_png(frame):
    val, image = cv2.imencode('.png', frame)
    return ''.join(struct.pack('B', byte[0]) for byte in image)


def get_rect(x, y, width, height, picture):
    return {'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'picture': picture}


sender = FaceSender()
sender.get_service_info("RingoHTTPMediaServer")
sender.set_auth('ringo', 'ringo-123')

capture = cv2.VideoCapture(-1)

while True:
    try:
        retVal, frame = capture.read()
    except cv2.error:
        print("Cannot read frame from capture device")
        break

    cv2.imshow('Ringo Capture', frame)

    key = 0xFF & cv2.waitKey(10)

    if key == 10: # Enter
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_face(gray_frame)

        if faces.size > 0:
            picture = sender.post_picture(frame_to_png(frame), 'png')

            rects = []
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
                rects.append(get_rect(x, y, w, h, picture))

            sender.post_rect(rects)
            sender.close()

            cv2.imshow('Face', frame)

    elif key == 27: # Escape
        break
