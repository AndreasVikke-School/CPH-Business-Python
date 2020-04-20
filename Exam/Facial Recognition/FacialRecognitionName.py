import FacialRecognitionLearner as frl
import numpy as np
import cv2
import sys

image_path = sys.argv[1]
image = cv2.imread(image_path)

def learn_faces():
    known_name_image = {
        "Andreas Vikke" : frl.face_encodings_data(cv2.imread('images/train/Vikke.jpg'))[0],
        "Frederik Holm" : frl.face_encodings_data(cv2.imread('images/train/Fred.jpg'))[0],
        "Martin Eli" : frl.face_encodings_data(cv2.imread('images/train/Martin.jpg'))[0],
        "Max Gade" : frl.face_encodings_data(cv2.imread('images/train/Max.jpg'))[0]
    }
    return known_name_image

def show_matches_on_image(known_name_image):
    face_locations = frl.face_location_data(image)
    face_encodings = frl.face_encodings_data(image, face_locations)

    for idx, ((t, r, b, l), face_encoding) in enumerate(zip(face_locations, face_encodings)):
        face_matches = frl.compare_faces(known_name_image, face_encoding, 0.62)

        face_name = "Unknown"

        face_distances = frl.face_distance(known_name_image, face_encoding)
        face_match_index = np.argmin(face_distances)
        if face_matches[face_match_index]:
            face_name = list(known_name_image.keys())[face_match_index]


        landmarks_as_tuples = frl.faces_landmarks_dict(image, face_locations)
        draw_on_image(t, r, b, l, face_name, landmarks_as_tuples[idx])        

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)

def draw_on_image(t, r, b, l, face_name, face_features):

    # Draw rectangle around face    
    cv2.rectangle(image, (l, t), (r, b), (0, 200, 0), 2)

    # Draw face fatures
    for points in face_features.values():
        for idx, point in enumerate(points):
            if idx+1 != len(points):
                cv2.line(image, (points[idx][0], points[idx][1]), (points[idx+1][0], points[idx+1][1]), (255,255,255), 1)

    # Draw Rectangle with name in
    height = 15*2
    cv2.rectangle(image, (l-1, t-height), (r+1, t+1), (0, 200, 0), -1)
    cv2.putText(image, face_name, 
        (l+5, t - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        height/(height+15),
        (255, 255, 255),
        1)

if __name__ == "__main__":
    known_name_image = learn_faces()
    show_matches_on_image(known_name_image)
    