#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy
import argparse
import math
import EyesFSM
import TanTriggs

cascade_dir = 'cascades'

face_cascade_files = ['lbpcascade_frontalface.xml',
                      'haarcascade_frontalface_alt_tree.xml',
                      'haarcascade_frontalface_alt.xml',
                      'haarcascade_frontalface_alt2.xml',
                      'haarcascade_frontalface_default.xml']

face_cascades = [cv2.CascadeClassifier(os.path.join(cascade_dir, c))
                 for c in face_cascade_files]

eyes_cascade_files = ['haarcascade_eye.xml',
                      'haarcascade_eye_tree_eyeglasses.xml',
                      'haarcascade_lefteye_2splits.xml',
                      'haarcascade_righteye_2splits.xml',
                      'haarcascade_mcs_lefteye.xml',
                      'haarcascade_mcs_righteye.xml']

eyes_cascades = [cv2.CascadeClassifier(os.path.join(cascade_dir, c))
                 for c in eyes_cascade_files]

# Silly cv2
CV_GUI_NORMAL = 0x10
CV_WINDOW_AUTOSIZE = 0x01

# Colors (in BGR system):
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

# Window names
MAIN_WINDOW = "Webcam"
FACE_WINDOW = "Face"
FINAL_FACE_WINDOW = "Final face"

FACE_OFFSET_Y = 30


def detect_feature(frame, cascade_list):
    """Try each cascade in cascade_list until it detects the object it is
    looking for"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for c in cascade_list:
        features = c.detectMultiScale(gray, minSize=(60, 60))
        if len(features) > 0:
            return features
    return numpy.empty(0)


def on_mouse_event(event, x, y, flags, (fsm, face)):
    """Process mouse events"""
    if event != cv2.EVENT_LBUTTONDOWN or fsm is None:
        return

    # Set the current eye to the mouse coordinates and advance the FSM to the
    # next state (i.e. the next eye)
    fsm.set_current_eye_pos((x, y))
    fsm.next()
    fsm.update_window(FACE_WINDOW, face)


def get_angle_from_eyes(eye_left, eye_right):
    # get the direction
    eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])

    # calc rotation angle in radians
    rotation = math.atan2(float(eye_direction[1]), float(eye_direction[0]))
    return rotation


def rotate(image, angle, center):
    rows, cols = image.shape
    rotation = cv2.getRotationMatrix2D(center, math.degrees(angle), 1)
    return cv2.warpAffine(image, rotation, (cols, rows))


def main_loop(directory):
    image_index = 0
    image = numpy.empty(0)

    # Open the default webcam
    capture = cv2.VideoCapture(0)

    while True:
        # Read a frame from the capture device and show it
        _, frame = capture.read()
        cv2.imshow(MAIN_WINDOW, frame)

        key = 0xFF & cv2.waitKey(10)

        if key == 13 or key == 10:  # Enter
            faces = detect_feature(frame, face_cascades)

            # We want just one face, because we're training the detector
            if faces.size == 4:
                x, y, w, h = faces[0]
                face_roi = frame[y:y + h, x:x + w]

                # Try to detect eyes in this face
                eyes = detect_feature(face_roi, eyes_cascades)

                # Create a window with custom attributes
                cv2.namedWindow(FACE_WINDOW, CV_WINDOW_AUTOSIZE | CV_GUI_NORMAL)

                # Initialize our state machine for the eyes
                eyes_fsm = EyesFSM.EyesFSM(face_roi.shape)

                # Setup a callback function for mouse events
                cv2.setMouseCallback(FACE_WINDOW, on_mouse_event, (eyes_fsm, face_roi))

                # Make a copy of the image to save it later
                image = frame.copy()

                # We only care about people with two eyes.
                if eyes.size == 8:
                    # Populate the state machine with the eyes just found
                    for e in eyes:
                        eyes_fsm.set_current_eye_pos(e)
                        eyes_fsm.next()

                # Update the window to show the eyes
                eyes_fsm.update_window(FACE_WINDOW, face_roi)

        elif key == ord('s') and image.size > 0 and eyes_fsm and eyes_fsm.is_valid():
            # Find a non-existing filename for the new image
            while True:
                filename = os.path.join(directory, '%s.png' % image_index)

                if not os.path.exists(filename):
                    break
                image_index += 1

            # Sort the eyes
            eyes_fsm.sort_eyes()

            # Get the eyes position relative to the frame from the face ROI
            eye_left = eyes_fsm.get_frame_coordinates(eyes_fsm.eyes[0], x, y)
            eye_right = eyes_fsm.get_frame_coordinates(eyes_fsm.eyes[1], x, y)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Rotate the whole frame to align eyes
            image = rotate(image, get_angle_from_eyes(eye_left, eye_right), eye_left)

            # Crop to the face
            image = image[y - FACE_OFFSET_Y: y + h + FACE_OFFSET_Y, x: x + w]

            # Rezise the face to a standard size
            image = cv2.resize(image, (260, 315), interpolation=cv2.INTER_CUBIC)

            print("Saving image to %s." % filename)
            cv2.imwrite(filename, image)

            # cv2.destroyWindow(FACE_WINDOW)
            cv2.imshow(FINAL_FACE_WINDOW, image)

            TanTriggs.tan_triggs(image)

            image_index += 1
            image = numpy.empty(0)

        elif key == 27:  # Escape
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("name",
                        help="Name of the subject for identification")
    parser.add_argument("-d", "--directory",
                        help="Directory in which to save the images. If it "
                             "doesn't exist, it will be created.",
                        default="photos")

    args = parser.parse_args()

    subject_dir = os.path.join(args.directory, args.name)

    # Create a directory for this subject if it doesn't exist already
    if not os.path.isdir(subject_dir):
        os.makedirs(subject_dir)

    info_file = "%s/info.txt" % subject_dir

    if not os.path.exists(info_file):
        full_name = raw_input("Enter subject's complete name: ")
        with open(info_file, "w") as f:
            f.write("name:%s" % full_name)

    main_loop(subject_dir)
