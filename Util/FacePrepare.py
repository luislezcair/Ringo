import os
import cv2
import numpy
import argparse
import CropFaces as cf
import EyesFSM
from PIL import Image


cascade_dir = '/usr/share/opencv/haarcascades'

face_cascade_files = ['haarcascade_frontalface_alt_tree.xml',
                      'haarcascade_frontalface_alt.xml',
                      'haarcascade_frontalface_alt2.xml',
                      'haarcascade_frontalface_default.xml',
                      'haarcascade_profileface.xml']

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


def detect_feature(frame, cascade_list):
    """Try each cascade in cascade_list until it detects the object it is
    looking for"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for c in cascade_list:
        features = c.detectMultiScale(gray, minSize=(30, 30))
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


def main_loop(subject_name, directory):
    image_index = 0
    image = numpy.empty(0)

    # Open the default webcam
    capture = cv2.VideoCapture(-1)

    while True:
        # Read a frame from the capture device and show it
        _, frame = capture.read()
        cv2.imshow(MAIN_WINDOW, frame)

        key = 0xFF & cv2.waitKey(10)

        if key == 13 or key == 10:  # Enter
            faces = detect_feature(frame, face_cascades)

            # We want just one face, because we're training the detector
            if faces.size == 4:
                for (x, y, w, h) in faces:
                    face_roi = frame[y:y + h, x:x + w]

                    eyes = detect_feature(face_roi, eyes_cascades)

                    # Create a window with custom attributes
                    cv2.namedWindow(FACE_WINDOW, CV_WINDOW_AUTOSIZE | CV_GUI_NORMAL)

                    # Initialize our state machine for the eyes
                    eyes_fsm = EyesFSM.EyesFSM(face_roi.shape)

                    # Setup a callback function for mouse events
                    cv2.setMouseCallback(FACE_WINDOW, on_mouse_event, (eyes_fsm, face_roi))

                    # Make a copy of the image to save it later
                    image = face_roi.copy()

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
                filename = os.path.join(directory,
                            '%s_%s.png' % (subject_name, image_index))

                if not os.path.exists(filename):
                    break
                image_index += 1

            # CropFaces expects a Pillow image, so convert to it
            rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)

            # Sort the eyes
            eyes_fsm.sort_eyes()

            print("Saving image to %s." % filename)
            cf.CropFace(pil_img,
                        eye_left=eyes_fsm.eyes[0],
                        eye_right=eyes_fsm.eyes[1],
                        offset_pct=(0.25, 0.25),
                        dest_sz=(200, 200)).save(filename)

            cv2.destroyWindow(FACE_WINDOW)
            image_index += 1
            image = numpy.empty(0)

        elif key == 27: # Escape
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

    main_loop(args.name, subject_dir)
