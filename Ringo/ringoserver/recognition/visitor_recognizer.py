import cv2
import numpy


CASCADE_FILE = 'ringoserver/recognition/lbpcascade_frontalface.xml'
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
        cv_picture = cv2.imread(picture.path)
        gray = cv2.cvtColor(cv_picture, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, minSize=(30, 30))

        result = []

        for (x, y, w, h) in faces:
            # Crop to the face Region of Interest
            face_roi = gray[y:y + h, x:x + w]

            prediction, confidence = self.model.predict(face_roi)
            if prediction >= 0:
                result.append((prediction, confidence))

        return result
