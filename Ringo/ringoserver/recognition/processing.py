#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import math
import numpy
import tantriggs


CASCADE_DIR = 'ringoserver/recognition/cascades'

FACE_CASCADE_FILES = ['lbpcascade_frontalface.xml',
                      'haarcascade_frontalface_alt_tree.xml',
                      'haarcascade_frontalface_alt.xml',
                      'haarcascade_frontalface_alt2.xml',
                      'haarcascade_frontalface_default.xml']

EYES_CASCADE_FILES = ['haarcascade_eye.xml',
                      'haarcascade_eye_tree_eyeglasses.xml',
                      'haarcascade_lefteye_2splits.xml',
                      'haarcascade_righteye_2splits.xml',
                      'haarcascade_mcs_lefteye.xml',
                      'haarcascade_mcs_righteye.xml']

FACE_CASCADES = [cv2.CascadeClassifier(os.path.join(CASCADE_DIR, c))
                 for c in FACE_CASCADE_FILES]

EYES_CASCADES = [cv2.CascadeClassifier(os.path.join(CASCADE_DIR, c))
                 for c in EYES_CASCADE_FILES]

FACE_OFFSET_Y = 30

FACE_WIDTH = 260
FACE_HEIGHT = 315


def detect_feature(frame, cascade_list):
    """Try each cascade in cascade_list until it detects the object it is
    looking for"""
    for cascade in cascade_list:
        features = cascade.detectMultiScale(frame, minSize=(60, 60))
        if len(features) > 0:
            return features
    return numpy.empty(0)


def get_angle_from_eyes(eye_left, eye_right):
    """Calculate the angle from the left eye to the right eye"""
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])

    # calc rotation angle in radians
    rotation = math.atan2(float(eye_direction[1]), float(eye_direction[0]))
    return rotation


def rotate(image, angle, center):
    """Rotate an image by angle degrees using center as the central point"""
    rows, cols = image.shape
    rotation = cv2.getRotationMatrix2D(center, math.degrees(angle), 1)
    return cv2.warpAffine(image, rotation, (cols, rows))


def get_center(s):
    """Returns the center of a square s, where s = (x, y, w, h)"""
    x, y, w, h = s
    return (x + w) / 2, (y + h) / 2


def sort_eyes(eyes):
    """Put the left eye first in the list and the right eye second"""
    x1 = eyes[0][0]
    x2 = eyes[1][0]

    if x1 > x2:
        eyes.reverse()


def to_frame_coordinates(eyes, face_x, face_y):
    x1, y1 = eyes[0]
    x2, y2 = eyes[1]
    return [(x1 + face_x, y1 + face_y), (x2 + face_x, y2 + face_y)]


def debug_save(image):
    """Save the processed image for debugging purposes"""
    # Find a non-existing filename for the new image
    index = 0
    filename = 'jondoe.png'
    while True:
        filename = 'media/visits/visit_%s.png' % index

        if not os.path.exists(filename):
            break
        index += 1

    cv2.imwrite(filename, image)


def process(picture_path):
    frame = cv2.imread(picture_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    faces_raw = detect_feature(frame, FACE_CASCADES)

    faces = []
    for (x, y, w, h) in faces_raw:
        image = frame.copy()

        # Crop to the face Region of Interest
        face_roi = image[y - FACE_OFFSET_Y:y + h + FACE_OFFSET_Y, x:x + w]

        # Try to detect eyes in this face
        face_eyes = detect_feature(face_roi, EYES_CASCADES)

        # If we find both eyes, calculate the center and rotate the frame to align the eyes
        if face_eyes.size == 8:
            eyes = [get_center(face_eyes[0]), get_center(face_eyes[1])]
            sort_eyes(eyes)

            eyes = to_frame_coordinates(eyes, x, y)
            image = rotate(image, get_angle_from_eyes(eyes[0], eyes[1]), eyes[0])

        # Crop to the face
        image = image[y - FACE_OFFSET_Y:y + h + FACE_OFFSET_Y, x:x + w]

        # Rezise the face to a standard size
        image = cv2.resize(image, (FACE_WIDTH, FACE_HEIGHT), interpolation=cv2.INTER_CUBIC)

        # Apply the Tan Triggs transformation
        image = tantriggs.tantriggs(image)

        debug_save(image)

        faces.append(image)

    return faces
