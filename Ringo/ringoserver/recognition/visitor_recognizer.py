import os
import cv2
import numpy
import processing
import logging
from django.conf import settings


LBP_RECOGNITION_THRESHOLD = 25.0

logging.basicConfig(level=logging.INFO)


class VisitorRecognizer:
    def __init__(self, visitor_faces):
        self.visitors = visitor_faces
        self.model = cv2.createLBPHFaceRecognizer(threshold=LBP_RECOGNITION_THRESHOLD)

    def _prepare_trainingset(self):
        labels = [sample.visitor.id for sample in self.visitors]
        images = [sample.picture for sample in self.visitors]

        images_gray = []
        for image in images:
            pic = cv2.imread(image.path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            images_gray.append(pic)

        return numpy.array(images_gray), numpy.array(labels)

    def train_model(self):
        """
        Load the training file if it exists. If not, train the model with the
        visitors from the database and save the training.
        """
        if os.path.exists(settings.RINGO_TRAINING_FILE):
            self.model.load(settings.RINGO_TRAINING_FILE)
            logging.info("Training file loaded")
        else:
            images, labels = self._prepare_trainingset()
            self.model.train(images, labels)
            self.model.save(settings.RINGO_TRAINING_FILE)
            logging.info("Training file not found. Training and saving...")

    def recognize_visitor(self, picture):
        result = []
        faces = processing.process(picture.path)

        for face in faces:
            prediction, confidence = self.model.predict(face)
            if prediction >= 0:
                result.append((prediction, confidence))

        return result, len(faces)
