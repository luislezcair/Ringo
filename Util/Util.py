import cv2


def detect_many_and_show(frame, cascade_list):
    """Show a window for every feature detected using every cascade in
    cascade_list"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    i = 0
    for c in cascade_list:
        features = c.detectMultiScale(gray, minSize=(30,30))
        frame_copy = frame.copy()
        for (x, y, w, h) in features:
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), RED, 1)
        i += 1
        cv2.imshow("Cascade %s" % i, frame_copy)
