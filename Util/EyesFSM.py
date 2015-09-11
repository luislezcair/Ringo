import cv2
import numpy


class EyesFSM():
    def __init__(self, shape):
        """Construct an EyesFSM with an internal frame with dimensions of 
        shape"""
        self.eyes = [(), ()]
        self.shape = shape
        self.state = 0
        self.new_frame()

    def next(self):
        """Advance the FSM to the next state"""
        self.state += 1
        if self.state > 1:
            self.state = 0

    def set_current_eye_pos(self, eye_pos):
        # If eye_pos has 4 coordinates it is a rect surrounding the eye. We need
        # to get the center
        self.eyes[self.state] = self.get_rect_center(eye_pos) if len(eye_pos) == 4 else eye_pos

    def sort_eyes(self):
        """Put the left eye first in the list and the right eye second"""
        x1 = self.eyes[0][0]
        x2 = self.eyes[1][0]

        if x1 > x2:
            self.eyes.reverse()

    def is_valid(self):
        """Returns True if the two eyes are set"""
        return self.eyes[0] and self.eyes[1]

    def new_frame(self):
        """Create a new empty frame in which to draw the eyes"""
        self.eyes_frame = numpy.zeros(self.shape, numpy.uint8)

    def draw_eyes(self):
        """Draw the eyes we have so far"""
        GREEN = (0, 255, 0)
        for eye in self.eyes:
            if eye:
                cv2.circle(self.eyes_frame, eye, 8, GREEN, 1)

    def show(self, window, frame):
        """Draw the eyes in a window over a frame"""
        cv2.imshow(window, cv2.add(frame, self.eyes_frame))

    def update_window(self, window, frame):
        """Draw the eyes in a window over a frame, display it and reset the
        internal frame"""
        self.draw_eyes()
        self.show(window, frame)
        self.new_frame()

    @staticmethod
    def get_rect_center(rect):
        """Returns the coordinates for the center of a rectangle"""
        x, y, w, h = rect
        return x + w/2, y + h/2

    @staticmethod
    def get_frame_coordinates(eye, face_x, face_y):
        return eye[0] + face_x, eye[1] + face_y
