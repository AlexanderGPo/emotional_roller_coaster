import numpy as np
import cv2
import pygame
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from sources.detecting_emotions import *

FACE_COLOR = (0, 255, 0)

base_options = python.BaseOptions(model_asset_path='sources/face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

GAME_STATUS = True

cap = cv2.VideoCapture(0)

WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emotional roller-coaster")

while cap.isOpened() and GAME_STATUS:
    ret, frame = cap.read()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            GAME_STATUS = False

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    surf_frame = pygame.surfarray.make_surface(np.rot90(imgRGB, 1))
    screen.blit(pygame.transform.flip(surf_frame, True, False), (0, 0))

    image_for_detection = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
    detection_result = detector.detect(image_for_detection)

    if len(detection_result.face_landmarks):
        if is_front_face(detection_result.face_landmarks[0]):
            FACE_COLOR = (0, 255, 0)

            if is_surprised(detection_result.face_landmarks[0]):
                print("surprised")

            if is_happy(detection_result.face_landmarks[0]):
                print("happy")

            if is_sceptic(detection_result.face_landmarks[0]):
                print("sceptic")

            if is_sad(detection_result.face_landmarks[0]):
                print("sad")

        else:
            FACE_COLOR = (255, 0, 0)
            print("bad face")

        for index, point in enumerate(detection_result.face_landmarks[0]):
            x_tip = int(point.x * imgRGB.shape[1])
            y_tip = int(point.y * imgRGB.shape[0])
            cv2.circle(imgRGB, (x_tip, y_tip), 1, FACE_COLOR, -1)
    else:
        print("no face")

    res_image = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

    pygame.display.flip()
    pygame.display.update()

