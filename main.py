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
    pose_connections_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    if detected_result.pose_landmarks:

        first_person_landmarks = detected_result.pose_landmarks[0]

        left_knee_index = 25
        right_knee_index = 26
        left_foot_index = 31
        right_foot_index = 32
        left_knee = first_person_landmarks[left_knee_index]
        right_knee = first_person_landmarks[right_knee_index]

        left_foot = first_person_landmarks[left_foot_index]
        right_foot = first_person_landmarks[right_foot_index]

        if left_knee.y < left_foot.y or right_knee.y < right_foot.y:
            cv.putText(annotated_image, 'Knee Up', (0, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
        if left_knee.visibility < 0.5 or right_knee.visibility < 0.5:
            cv.putText(annotated_image, 'Knee Down', (0, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)


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