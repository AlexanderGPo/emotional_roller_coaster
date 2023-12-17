import numpy as np
import cv2

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import emoji

from sources.detecting_emotions import*

FACE_COLOR = (0, 255, 0)

base_options = python.BaseOptions(model_asset_path='sources/face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_for_detection = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
    detection_result = detector.detect(image_for_detection)

    if len(detection_result.face_landmarks):
        if is_front_face(detection_result.face_landmarks[0]):
            FACE_COLOR = (0, 255, 0)

            if is_surprised(detection_result.face_landmarks[0]):
                print("surprised")

        else:
            FACE_COLOR = (255, 0, 0)

        for point in detection_result.face_landmarks[0]:
            x_tip = int(point.x * imgRGB.shape[1])
            y_tip = int(point.y * imgRGB.shape[0])
            cv2.circle(imgRGB, (x_tip, y_tip), 1, FACE_COLOR, -1)
    else:
        print("no face")
    res_image = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)
