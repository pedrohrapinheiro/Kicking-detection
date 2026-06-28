import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision

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