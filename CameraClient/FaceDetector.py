import os
import cv2
import numpy
import struct
from FaceSender import FaceSender


cascade_dir = 'cascades/'

cascade_files = ['lbpcascade_frontalface.xml',
                 'haarcascade_frontalface_alt_tree.xml',
                 'haarcascade_frontalface_alt.xml',
                 'haarcascade_frontalface_alt2.xml',
                 'haarcascade_frontalface_default.xml']

cascades = [cv2.CascadeClassifier(os.path.join(cascade_dir, c))
            for c in cascade_files]


def detect_face(frame):
    """Try each cascade in the list until a face is found"""
    for c in cascades:
        faces = c.detectMultiScale(frame, minSize=(40, 40))
        if len(faces) > 0:
            return faces
    return numpy.empty(0)


def frame_to_png(frame):
    """Encode the frame in png and convert it to an array of bytes"""
    val, image = cv2.imencode('.png', frame)
    return ''.join(struct.pack('B', byte[0]) for byte in image)


def get_rect(x, y, width, height, picture):
    """Construct a dictionary with the values passed"""
    return {'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'picture': picture}


sender = FaceSender()
# sender.get_service_info("RingoHTTPMediaServer")
sender.set_auth('ringo', 'ringo-123')

capture = cv2.VideoCapture(0)

GREEN = (0, 255, 0)

while True:
    _, frame = capture.read()

    cv2.imshow('Ringo Capture', frame)

    key = 0xFF & cv2.waitKey(10)

    if key == 13 or key == 10:  # Enter
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_face(gray_frame)

        if faces.size > 0:
            # If we have a face, send the picture and wait for the reply which
            # contains the URL assigned to the picture.
            picture = sender.post_picture(frame_to_png(frame), 'png')

            # Append each rect to the list along with the picture URL obtained
            # before
            rects = []
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), GREEN, 1)
                rects.append(get_rect(x, y, w, h, picture))

            # Send the rects
            sender.post_rect(rects)
            sender.close()

            cv2.imshow('Face', frame)

    elif key == 27:  # Escape
        break
