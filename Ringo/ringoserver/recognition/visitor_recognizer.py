import cv2
import numpy
import processing


CASCADE_FILE = 'ringoserver/recognition/cascades/lbpcascade_frontalface.xml'
LBP_RECOGNITION_THRESHOLD = 110.0


class VisitorRecognizer:
    def __init__(self, visitor_faces):
        self.visitors = visitor_faces
        self.model = cv2.createLBPHFaceRecognizer(threshold=LBP_RECOGNITION_THRESHOLD)
        self.face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

    def _prepare_trainingset(self):
        labels = [sample.visitor.id for sample in self.visitors]
        images = [sample.picture for sample in self.visitors]

        images_gray = []
        for image in images:
            pic = cv2.imread(image.path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            images_gray.append(pic)

        return numpy.array(images_gray), numpy.array(labels)

    def train_model(self):
        # TODO: save the training set and load it here: model.save() & model.load()

        images, labels = self._prepare_trainingset()
        self.model.train(images, labels)

    def recognize_visitor(self, picture):
        result = []
        faces = processing.process(picture.path)

        for face in faces:
            prediction, confidence = self.model.predict(face)
            if prediction >= 0:
                result.append((prediction, confidence))

        return result
