import numpy as np
import cv2
import random
import pygame
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from sources.detecting_emotions import *
from sources.visual_aids import *

FACE_COLOR = (0, 255, 0)

base_options = python.BaseOptions(model_asset_path='sources/face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emotional roller-coaster")

FPS = 30
fps_timer = pygame.time.Clock()
last_update = pygame.time.get_ticks()

GAME_STATUS = True
RECOGNITION_STATUS = False
TIME_FOR_EMOTION = 5000
SCORE = 0
PREV_BORDER = 0
WRONG_ANS = 0
CURRENT_EMOTION = -1
EMOTIONS = ['surprised', 'happy', 'sceptic', 'sad']

while cap.isOpened() and GAME_STATUS:
    ret, frame = cap.read()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            GAME_STATUS = False
        elif e.type == pygame.KEYDOWN:
            RECOGNITION_STATUS = True
            TIME_FOR_EMOTION = 5000
            SCORE = 0
            PREV_BORDER = 0
            WRONG_ANS = 0
            CURRENT_EMOTION = random.randint(1, 4)

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    surf_frame = pygame.surfarray.make_surface(np.rot90(imgRGB, 1))
    screen.blit(pygame.transform.flip(surf_frame, True, False), (0, 0))

    image_for_detection = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
    detection_result = detector.detect(image_for_detection)
    if len(detection_result.face_landmarks):
        if is_front_face(detection_result.face_landmarks[0]):
            FACE_COLOR = (0, 255, 0)
            if RECOGNITION_STATUS:
                now = pygame.time.get_ticks()

                cur_status = -1
                if is_surprised(detection_result.face_landmarks[0]):
                    cur_status = 1
                elif is_happy(detection_result.face_landmarks[0]):
                    cur_status = 2
                elif is_sceptic(detection_result.face_landmarks[0]):
                    cur_status = 3
                elif is_sad(detection_result.face_landmarks[0]):
                    cur_status = 4

                if cur_status == CURRENT_EMOTION:
                    SCORE += 1
                    if SCORE > PREV_BORDER + 10:
                        TIME_FOR_EMOTION = max(500, TIME_FOR_EMOTION - 500)
                        PREV_BORDER = SCORE

                if now - last_update > TIME_FOR_EMOTION or cur_status == CURRENT_EMOTION:
                    if cur_status != CURRENT_EMOTION:
                        WRONG_ANS += 1
                        if WRONG_ANS > 10:
                            RECOGNITION_STATUS = False
                    last_update = now
                    temp = random.randint(1, 4)
                    while temp == CURRENT_EMOTION:
                        temp = random.randint(1, 4)
                    CURRENT_EMOTION = temp
        else:
            FACE_COLOR = (255, 0, 0)
            RECOGNITION_STATUS = False

        if not RECOGNITION_STATUS:
            for index, point in enumerate(detection_result.face_landmarks[0]):
                x_tip = int(point.x * imgRGB.shape[1])
                y_tip = int(point.y * imgRGB.shape[0])
                pygame.draw.circle(screen,  FACE_COLOR, (x_tip, y_tip), 1)
    else:
        print("no face")

    if not RECOGNITION_STATUS:
        status = DAX_PRO_36.render("tap to start", True, (180, 0, 0))
        screen.blit(status, (WIDTH // 2 - 20, 10))
    else:
        cur_emotion = DAX_PRO_36.render(f'new emotion {EMOTIONS[CURRENT_EMOTION - 1]}', True, (180, 0, 0))
        screen.blit(cur_emotion, (10, 10))

        cur_score = DAX_PRO_36.render(f'score is {SCORE}', True, (180, 0, 0))
        screen.blit(cur_score, (WIDTH - 200, 10))

        cur_time = DAX_PRO_36.render(f'wrongs are {WRONG_ANS}', True, (180, 0, 0))
        screen.blit(cur_time, (WIDTH - 200, 50))

    res_image = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

    pygame.display.flip()
    pygame.display.update()

    fps_timer.tick(FPS)

pygame.quit()
