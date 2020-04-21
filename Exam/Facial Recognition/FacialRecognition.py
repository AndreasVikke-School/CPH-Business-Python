import FacialRecognitionDraw as frld
import numpy as np
import argparse
import sys
import cv2
import os

def video_capture(args):
    camera = 0
    if args.camera.isdigit(): 
        camera = int(args.camera)
    else:
        if os.path.isfile(args.camera):
            camera = args.camera
        else:
            raise ConnectionError("Camera must be an integer or an existing file")

    cap = cv2.VideoCapture(camera)
    known_name_images = frld.learn_faces()

    process_frame = True
    draw_features = args.features

    is_image = False
    if not args.camera.isdigit():
        is_image = camera.split('.')[1] in ['jpg', 'png', 'jpeg']

    while(True):
        # Capture frame-by-frame
        if is_image:
            frame = cv2.imread(camera)
        else:
            ret, frame = cap.read()

        if process_frame:
            frame = frld.show_matches_on_image(known_name_images, frame, upscale=1 if is_image else 4, draw_features=draw_features, tolerance=float(args.tolerance))

        # Display the resulting frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that records the video camera and shows facial recognition. Press q to quit the program.')
    parser.add_argument('camera', help='an int for the camera or a string of the filename to show')
    parser.add_argument('-f', '--features', default=False, help='a boolean if features of the face should be drawn')
    parser.add_argument('-t', '--tolerance', default=0.63, help='an integer for the tolerance of distance between face matches')
    args = parser.parse_args()

    video_capture(args)