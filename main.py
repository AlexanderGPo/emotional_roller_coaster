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
        no_face_surf_1 = pygame.image.load('sources/img/no.png')
        no_face_rect_1 = no_face_surf_1.get_rect()
        no_face_rect_1.right = WIDTH // 2 - 10
        no_face_rect_1.centery = HEIGHT // 2
        no_face_surf_2 = pygame.image.load('sources/img/face.png')
        no_face_rect_2 = no_face_surf_2.get_rect()
        no_face_rect_2.left = WIDTH // 2 + 10
        no_face_rect_2.centery = HEIGHT // 2
        screen.blit(no_face_surf_1, no_face_rect_1)
        screen.blit(no_face_surf_2, no_face_rect_2)

    if not RECOGNITION_STATUS:
        info_surf = pygame.image.load('sources/img/keyboard.png')
        info_rect_1 = info_surf.get_rect()
        info_rect_1.right = WIDTH // 2 - 100
        info_rect_2 = info_surf.get_rect()
        info_rect_2.centerx = WIDTH // 2
        info_rect_3 = info_surf.get_rect()
        info_rect_3.left = WIDTH // 2 + 100
        screen.blit(info_surf, info_rect_1)
        screen.blit(info_surf, info_rect_2)
        screen.blit(info_surf, info_rect_3)
    else:
        emotion_surf = pygame.image.load(f'sources/img/emotion{CURRENT_EMOTION}.png')
        emotion_rect = emotion_surf.get_rect()
        emotion_rect.centerx = WIDTH // 2
        emotion_rect.top = 10
        screen.blit(emotion_surf, emotion_rect)

        score_surf = pygame.image.load('sources/img/good_ans.png')
        score_surf = pygame.transform.scale(score_surf, (40, 40))
        score_rect = score_surf.get_rect()
        score_rect.left = WIDTH - 50
        score_rect.top = 10
        screen.blit(score_surf, score_rect)

        wrongs_surf = pygame.image.load('sources/img/bad_ans.png')
        wrongs_surf = pygame.transform.scale(wrongs_surf, (40, 40))
        wrongs_rect = wrongs_surf.get_rect()
        wrongs_rect.left = WIDTH - 50
        wrongs_rect.top = 60
        screen.blit(wrongs_surf, wrongs_rect)

        score_text = DAX_PRO_36.render(str(SCORE), True, (136, 189, 75))
        screen.blit(score_text, (WIDTH - 70 - 10 * len(str(SCORE)), 7))

        wrongs_text = DAX_PRO_36.render(str(WRONG_ANS), True, (155, 64, 64))
        screen.blit(wrongs_text, (WIDTH - 70 - 10 * len(str(WRONG_ANS)), 57))

    res_image = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

    pygame.display.flip()
    pygame.display.update()

    fps_timer.tick(FPS)

pygame.quit()
