import cv2
import sys
import os
import argparse
import numpy
import processing


LBP_RECOGNITION_THRESHOLD = 25


def parse_csv(filename):
    images_gray = []
    labels = []

    with open(filename) as csv:
        for line in csv:
            image_file, label = line.split(";")

            image = cv2.imread(image_file, cv2.CV_LOAD_IMAGE_GRAYSCALE)

            label = int(label)

            images_gray.append(image)
            labels.append(label)

    return images_gray, labels


def main_loop(training_file, testing_file, use_ff=False):
    # Parse the CSV file
    images_gray, labels = parse_csv(training_file)
    test_images, test_labels = parse_csv(testing_file)

    # Create the appropriate model for recognition
    if use_ff:
        model = cv2.createFisherFaceRecognizer()
    else:
        model = cv2.createLBPHFaceRecognizer(threshold=LBP_RECOGNITION_THRESHOLD)

    # Train the model with the gray-scale images and the labels
    print("Training the recognizer..."),
    sys.stdout.flush()

    model.train(numpy.array(images_gray), numpy.array(labels))

    print("OK.")

    # Statistics
    recognized_faces_good = 0
    unknowns = 0

    for s in range(0, len(test_labels)):
        image = processing.process(test_images[s])

        for i in image:
            prediction, confidence = model.predict(i)
            print("PREDICTED: %d, REAL: %d, CONFIDENCE: %s" % (prediction, test_labels[s], confidence))

            if prediction == test_labels[s]:
                recognized_faces_good += 1
            if prediction < 0:
                unknowns += 1

    total = len(test_labels)
    print("Well predicted faces: %s of %s total." % (recognized_faces_good, total))
    print("Desconocidos: %d" % unknowns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--training-set",
                        help="CSV file to train the detector",
                        default="training_set.csv")
    parser.add_argument("--testing-set",
                        help="CSV file with images to test recognition",
                        default="testing_set.csv")
    parser.add_argument("-f", "--fisherfaces",
                        help="Use FisherFaces method for face recognition "
                        "instead of LBP",
                        action="store_true")

    args = parser.parse_args()

    if not os.path.exists(args.training_set):
        print("CSV file '%s' not found." % args.training_set)
        sys.exit(1)

    if not os.path.exists(args.testing_set):
        print("CSV file '%s' not found." % args.testing_set)
        sys.exit(1)

    print("Using CSV file %s for TRAINING." % args.training_set)
    print("Using CSV file %s for TESTING." % args.testing_set)

    if args.fisherfaces:
        print("Using FisherFaces method for face recognition")
    else:
        print("Using Local Binary Patterns (LBP) method for face recognition")

    main_loop(args.training_set, args.testing_set, args.fisherfaces)
