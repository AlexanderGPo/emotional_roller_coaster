EPS = 0.1


def find_difference(face_landmarks: list, index_1, index_2, axis):
    if axis == "x":
        return abs(face_landmarks[index_1].x - face_landmarks[index_2].x)
    if axis == "y":
        return abs(face_landmarks[index_1].y - face_landmarks[index_2].y)
    if axis == "z":
        return abs(face_landmarks[index_1].z - face_landmarks[index_2].z)


def is_front_face(face_landmarks: list):
    if (find_difference(face_landmarks, 234, 454, 'z') > EPS or
            find_difference(face_landmarks, 10, 152, 'z') > EPS):
        return False
    return True


def is_surprised(face_landmarks: list):
    if (find_difference(face_landmarks, 0, 17, 'y') -
            find_difference(face_landmarks, 78, 306, 'x') > (EPS / 5)
            and (find_difference(face_landmarks, 33, 155, 'x') /
                 find_difference(face_landmarks, 159, 145, 'y')) < 2.5
            and (find_difference(face_landmarks, 362, 263, 'x') /
                 find_difference(face_landmarks, 368, 374, 'y')) < 2.5):
        return True
    else:
        return False


def is_happy(face_landmarks: list):
    if ((find_difference(face_landmarks, 78, 306, 'x') /
         find_difference(face_landmarks, 98, 460, 'x')) > 1.65
            and (face_landmarks[78].y < face_landmarks[12].y)
            and (face_landmarks[306].y < face_landmarks[12].y)):
        return True
    else:
        return False


def is_sceptic(face_landmarks: list):
    if (find_difference(face_landmarks, 52, 295, 'y') > (EPS / 10) >
            find_difference(face_landmarks, 78, 14, 'y')
            and find_difference(face_landmarks, 306, 14, 'y') < (EPS / 10)):
        return True
    else:
        return False


def is_suspicious(face_landmarks: list):
    if False:
        return True
    else:
        return False
