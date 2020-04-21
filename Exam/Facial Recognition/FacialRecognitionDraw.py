import FacialRecognitionData as frd
import numpy as np
import cv2
import sys

def learn_faces():
    """
        Learn Predefined Faces and return the encodings of them
    """

    known_name_images = {
        "Andreas Vikke" : frd.face_encodings_data(cv2.imread('images/train/Vikke.jpg'))[0],
        "Frederik Holm" : frd.face_encodings_data(cv2.imread('images/train/Fred.jpg'))[0],
        "Martin Eli" : frd.face_encodings_data(cv2.imread('images/train/Martin.jpg'))[0],
        "Max Gade" : frd.face_encodings_data(cv2.imread('images/train/Max.jpg'))[0],
        "Lars" : frd.face_encodings_data(cv2.imread('images/train/lam.jpg'))[0]
    }
    return known_name_images

def show_matches_on_image(known_name_images, image, upscale=1, draw_features=False, tolerance=0.63):
    """
        Finds matches of people on image and draws rectangles, names and fatures on the image

        :param known_name_images: known names and encodings for people
        :param image: image to be drawn ontop
        :param upscale: Optionally upsacle image times this after drawing
        :param draw_features: Optionally if face features should be drawn on image
    """

    if upscale > 1:
        small_image = cv2.resize(image, (0, 0), fx=1/upscale, fy=1/upscale)
    else:
        small_image = image

    face_locations = frd.face_location_data(small_image)
    face_encodings = frd.face_encodings_data(small_image, face_locations)

    for idx, ((t, r, b, l), face_encoding) in enumerate(zip(face_locations, face_encodings)):
        face_matches = frd.compare_faces(known_name_images, face_encoding, tolerance)

        face_name = "Unknown"

        face_distances = frd.face_distance(known_name_images, face_encoding)
        face_match_index = np.argmin(face_distances)
        if face_matches[face_match_index]:
            face_name = list(known_name_images.keys())[face_match_index]


        landmarks_as_tuples = frd.faces_landmarks_dict(small_image, face_locations)
        draw_on_image(t, r, b, l, face_name, landmarks_as_tuples[idx], image, upscale=upscale, draw_features=draw_features)        
    return image

def draw_on_image(t, r, b, l, face_name, face_features, image, upscale=1, draw_features=False):
    """
        Draws the stuff on the image

        :param (t, r, b, l): top, right, bottom, left cords of face rectangle
        :param face_name: name of the person of the face
        :param face_features: features of the face to draw
        :param image: image to draw ontop
        :param upscale: Optionally upsacle image times this after drawing
        :param draw_features: Optionally if face features should be drawn on image
    """

    # Upscale the cords to match the image
    (t, r, b, l) = (t*upscale, r*upscale, b*upscale, l*upscale)

    # Draw rectangle around face
    cv2.rectangle(image, (l, t), (r, b), (0, 200, 0), 2)

    # Draw face features
    if draw_features:
        for points in face_features.values():
            for idx, point in enumerate(points):
                if idx+1 != len(points):
                    cv2.line(image, (points[idx][0]*upscale, points[idx][1]*upscale), (points[idx+1][0]*upscale, points[idx+1][1]*upscale), (255,255,255), 1)

    # Draw Rectangle with name in
    height = 30
    cv2.rectangle(image, (l-1, t-height), (r+1, t), (0, 200, 0), cv2.FILLED)
    cv2.putText(image, face_name, 
        (l+6, t - 6), 
        cv2.FONT_HERSHEY_DUPLEX, 
        height/(height+15),
        (255, 255, 255),
        1)

if __name__ == "__main__":
    image_path = sys.argv[1]
    image = cv2.imread(image_path)
    known_name_image = learn_faces()
    show_matches_on_image(known_name_image, image)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)
    