import os
import cv2
import numpy
import argparse
import CropFaces as cf
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


def detect_feature(frame, cascade_list):
    """Try each cascade in cascade_list until it detects the object it is
    looking for"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for c in cascade_list:
        features = c.detectMultiScale(gray, minSize=(30, 30))
        if len(features) > 0:
            return features
    return numpy.empty(0)


def detect_many_and_show(frame, cascade_list):
    """Show a window for every feature detected using every cascade in
    cascade_list"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    i = 0
    for c in cascade_list:
        features = c.detectMultiScale(gray, minSize=(30,30))
        frame_copy = frame.copy()
        for (x, y, w, h) in features:
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), (0, 0, 255), 1)
        i += 1
        cv2.imshow("Cascade %s" % i, frame_copy)


def main_loop(subject_name, directory):
    image_index = 0
    image = numpy.empty(0)

    # Silly cv2
    CV_GUI_NORMAL = 0x10
    CV_WINDOW_AUTOSIZE = 0x01

    # Colors (in BGR system):
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)

    # Open the default webcam
    capture = cv2.VideoCapture(-1)

    while True:
        _, frame = capture.read()

        cv2.imshow('Ringo Capture', frame)

        key = 0xFF & cv2.waitKey(10)

        if key == 13 or key == 10: # Enter
            faces = detect_feature(frame, face_cascades)

            # We want just one face, because we're training the detector
            if faces.size == 4:
                for (x, y, w, h) in faces:
                    face_roi = frame[y:y + h, x:x + w]

                    eyes = detect_feature(face_roi, eyes_cascades)

                    # We only care about people with two eyes.
                    if eyes.size == 8:
                        # Make a copy of the image to save it later
                        image = face_roi.copy()

                        x1,  y1,  w1,  h1 = eyes[0]
                        x2,  y2,  w2,  h2 = eyes[1]

                        # The first element might not be the left eye, so make 
                        # sure the left eye is to the left and get the center
                        if x1 < x2:
                            eye_left = (x1 + w1/2, y1 + h1/2)
                            eye_right = (x2 + w2/2, y2 + h2/2)
                        else:
                            eye_left = (x2 + w2/2, y2 + h2/2)
                            eye_right = (x1 + w1/2, y1 + h1/2)

                        # Draw a rectangle around each eye
                        cv2.rectangle(face_roi, (x1, y1), (x1 + w1, y1 + w1), BLUE, 1)
                        cv2.rectangle(face_roi, (x2, y2), (x2 + w2, y2 + w2), BLUE, 1)

                        # Draw a circle in the center of the rectangle (the eye itself)
                        cv2.circle(face_roi, eye_left, 3, GREEN)
                        cv2.circle(face_roi, eye_right, 3, RED)

                        cv2.namedWindow('Face', CV_WINDOW_AUTOSIZE | CV_GUI_NORMAL)
                        cv2.imshow('Face', face_roi)

        elif key == ord('s') and image.size > 0:
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

            print("Saving image to %s." % filename)
            cf.CropFace(pil_img,
                        eye_left=eye_left,
                        eye_right=eye_right,
                        offset_pct=(0.25, 0.25),
                        dest_sz=(200, 200)).save(filename)

            cv2.destroyWindow('Face')
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
