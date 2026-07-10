import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import mediapipe as mp
from mediapipe.tasks import python
import cv2 as cv
from utils import drawing_landmarks, kick_analyzer

base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

previous_angle_left = None
previous_angle_right = None

cap = cv.VideoCapture("kicking.mp4")
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb
    )

    detected_result = detector.detect(mp_image)

    annotated_image = drawing_landmarks(mp_image.numpy_view(), detected_result)

    annotated_image, previous_angle_left, previous_angle_right = kick_analyzer(annotated_image, detected_result, previous_angle_left, previous_angle_right)

    cv.imshow('Output', cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()