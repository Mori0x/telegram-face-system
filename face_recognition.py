import cv2
from deepface import DeepFace

face_match = False
ban_face = False
no_flood = True

reference_img = cv2.imread("your_photo.jpg")
ban_img = cv2.imread("banned_photo.jpg")


def setup_face_recognition(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    def check_face(frame):
        global face_match, ban_face, no_flood
        try:
            if DeepFace.verify(frame, ban_img.copy())['verified']:
                no_flood = True
                ban_face = True
                return
            elif DeepFace.verify(frame, reference_img.copy())['verified']:
                face_match = True
            else:
                face_match = False
                ban_face = False
        except ValueError:
            face_match = False

    return cap, check_face
