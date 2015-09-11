import cv2
import os
import argparse
import numpy


# Define some colors (in BGR)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)

LBP_RECOGNITION_THRESHOLD = 110.0

def parse_csv(filename):
    images_gray = []
    labels = []
    names = {}

    with open(filename) as csv:
        for line in csv:
            image_file, label, name = line.split(";")

            image = cv2.imread(image_file, cv2.CV_LOAD_IMAGE_GRAYSCALE)

            label = int(label)

            images_gray.append(image)
            labels.append(label)
            names[label] = name.strip()

    images_gray = numpy.array(images_gray)
    labels = numpy.array(labels)

    return images_gray, labels, names


def main_loop(csv_file, use_ff=False):
    # Open the cascade file and create the classifier
    cascade_file = 'cascades/lbpcascade_frontalface.xml'
    lbp_cascade = cv2.CascadeClassifier(cascade_file)

    # Parse the CSV file
    images_gray, labels, names = parse_csv(csv_file)

    # Create the appropriate model for recognition
    if use_ff:
        model = cv2.createFisherFaceRecognizer()
    else:
        model = cv2.createLBPHFaceRecognizer(threshold=LBP_RECOGNITION_THRESHOLD)

    # Train the model with the gray-scale images and the labels
    model.train(images_gray, labels)

    # Open the default capture device (webcam)
    capture = cv2.VideoCapture(-1)

    while True:
        _, frame = capture.read()

        key = 0xFF & cv2.waitKey(10)
        if key == 27:
            break

        elif key == 13 or key == 10:
            # Convert the captured frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Try to detect faces
            faces = lbp_cascade.detectMultiScale(gray, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Crop to the face Region of Interest
                face_roi = gray[y:y + h, x:x + w]

                # Only for fisher faces and eigen faces resize the face
                face_resized = cv2.resize(face_roi, (92, 112), 1, 1, cv2.INTER_CUBIC)
                if use_ff:
                    # face_resized = cv2.resize(face_roi, (92, 112), 1, 1, cv2.INTER_CUBIC)
                    prediction, confidence = model.predict(face_resized)
                else:
                    # prediction, confidence = model.predict(face_roi)
                    prediction, confidence = model.predict(face_resized)

                name = "Desconocido" if prediction < 0 else names[prediction]

                # Draw the predicted name and confidence above the face
                text = "Prediction = %s Confidence = %s" % (name, confidence)
                cv2.putText(frame, text, (x - 15, y - 15), cv2.FONT_HERSHEY_PLAIN, 1.0, BLUE, 2)

                # Draw a rectangle around the face
                cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 1)

                cv2.imshow('Processed face', face_resized)

            cv2.imshow('Face', frame)

        cv2.imshow('LBPTest', frame)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv-file",
                        help="CSV file to train the detector",
                        default="faces.csv")
    parser.add_argument("-f", "--fisherfaces",
                        help="Use FisherFaces method for face recognition "
                        "instead of LBP",
                        action="store_true")

    args = parser.parse_args()

    print("Using CSV file %s" % args.csv_file)

    if args.fisherfaces:
        print("Using FisherFaces method for face recognition")
    else:
        print("Using Local Binary Patterns (LBP) method for face recognition")

    if os.path.exists(args.csv_file):
        main_loop(args.csv_file, args.fisherfaces)
    else:
        print("CSV file '%s' not found." % args.csv_file)
