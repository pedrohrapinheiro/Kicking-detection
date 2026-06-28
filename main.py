import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import mediapipe as mp
from mediapipe.tasks import python
import cv2 as cv

def drawing_landmarks(imageRGB, detected_result):
    pose_landmarks_list = detected_result.pose_landmarks
    annotated_image = np.copy(imageRGB)

    pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
    pose_connections_style = drawing_utils.DrawingSpec(color=(80, 22, 10), thickness=2)

    for landmarks in pose_landmarks_list:
        drawing_utils.draw_landmarks(
            annotated_image,
            landmarks,
            vision.PoseLandmarksConnections.POSE_LANDMARKS,
            pose_landmark_style,
            pose_connections_style)
    return annotated_image

base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

cap = cv.VideoCapture(0)

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

    cv.imshow('Output', cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()