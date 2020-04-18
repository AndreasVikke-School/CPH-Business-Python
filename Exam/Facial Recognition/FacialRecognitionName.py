import cv2
import dlib
import sys
import numpy as np

image_path = sys.argv[1]
casc_path = "./haarcascade_frontalcatface.xml"
image = cv2.imread(image_path)

predictor_68_point_model = "./models/shape_predictor_68_face_landmarks.dat"
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

face_recognition_model = "./models/dlib_face_recognition_resnet_model_v1.dat"
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

def _rect_to_cords(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def _cv2rect_to_cords(cv2rect):
    return cv2rect[1], cv2rect[0]+cv2rect[2], cv2rect[1]+cv2rect[3], cv2rect[0]

def _landmarks_data(faces):
    return [pose_predictor_68_point(image, face_location) for face_location in faces]

def draw_rects_on_image_cv2():
    face_detector = cv2.CascadeClassifier(casc_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for cv2rect in faces:
        (t, r, b, l) = _cv2rect_to_cords(cv2rect)
        cv2.rectangle(image, (l, t), (r, b), (0, 255, 0), 2)
    
    return faces

def draw_rects_on_image():
    face_detector = dlib.get_frontal_face_detector()

    faces = face_detector(image, 1)

    for rect in faces:
        (t, r, b, l) = _rect_to_cords(rect)
        cv2.rectangle(image, (l, t), (r, b), (0, 255, 0), 2)
    
    return faces

def draw_featues_on_image(faces):
    landmarks_as_tuples = [[(p.x, p.y) for p in landmark.parts()] for landmark in _landmarks_data(faces)]

    for face in _point_to_dict(landmarks_as_tuples):
        for name in face:
            points = face[name]
            for idx, point in enumerate(points):
                if idx+1 != len(points):
                    cv2.line(image, (points[idx][0], points[idx][1]), (points[idx+1][0], points[idx+1][1]), (255,255,255), 1)

def _point_to_dict(landmarks_as_tuples):
    return [{
            "chin": points[0:17],
            "left_eyebrow": points[17:22],
            "right_eyebrow": points[22:27],
            "nose_bridge": points[27:31],
            "nose_tip": points[31:36],
            "left_eye": points[36:42],
            "right_eye": points[42:48],
            "top_lip": points[48:55] + [points[64]] + [points[63]] + [points[62]] + [points[61]] + [points[60]],
            "bottom_lip": points[54:60] + [points[48]] + [points[60]] + [points[67]] + [points[66]] + [points[65]] + [points[64]]
        } for points in landmarks_as_tuples]

def _learn_face(image_path):
    person_image = cv2.imread(image_path)

    face_detector = dlib.get_frontal_face_detector()
    faces = face_detector(person_image, 1)
    landmarks = _landmarks_data(faces)

    encodings = [np.array(face_encoder.compute_face_descriptor(person_image, raw_landmark_set, 1)) for raw_landmark_set in landmarks]
    return encodings

def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

def draw_names_on_image(faces, name, idx):
        (t, r, b, l) = _rect_to_cords(faces[idx])
        cv2.rectangle(image, (l, t-15*2), (r, t), (0, 255, 0), -1)
        cv2.putText(image, name, 
            (l+5, t - 13), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.6,
            (255, 255, 255),
            1)

if __name__ == "__main__":
    vikke_face_encoding = _learn_face('Images/Vikke.jpg')[0]
    fred_face_encoding = _learn_face('Images/Fred.jpg')[0]
    martin_face_encoding = _learn_face('Images/Martin.jpg')[0]
    
    known_face_encodings = [
        vikke_face_encoding,
        fred_face_encoding,
        martin_face_encoding
    ]
    known_face_names = [
        "Andreas Vikke",
        "Fredrik Holm",
        "Martin Frederiksen"
    ]

    faces = draw_rects_on_image()
    draw_featues_on_image(faces)

    for idx, face in enumerate(faces):
        face_distances = face_distance(known_face_encodings, _learn_face(image_path)[idx])
        matches = list(face_distances <= 0.6)

        name = "Unknown"

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        draw_names_on_image(faces, name, idx)


    cv2.imshow("Faces found", image)
    cv2.waitKey(0)