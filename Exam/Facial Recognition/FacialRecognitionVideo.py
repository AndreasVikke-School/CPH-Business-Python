import FacialRecognitionLearner as frl
import FacialRecognitionDraw as frld
import numpy as np
import cv2

def video_capture():
    cap = cv2.VideoCapture(2)
    known_name_image = frld.learn_faces()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        image = frld.show_matches_on_image(known_name_image, frame)

        # Display the resulting frame
        cv2.imshow('Frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_capture()