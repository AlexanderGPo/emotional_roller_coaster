EPS = 0.1


def is_front_face(face_landmarks: list):
    if (abs(face_landmarks[234].z - face_landmarks[454].z) > EPS or
            abs(face_landmarks[10].z - face_landmarks[152].z) > EPS):
        return False
    return True
