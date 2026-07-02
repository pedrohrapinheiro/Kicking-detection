import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import cv2 as cv

def calculate_angle(a, b, c):

    radians = np.arctan2(c.y - b.y, c.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x)
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def drawing_landmarks(imageRGB, detected_result):
    pose_landmarks_list = detected_result.pose_landmarks

    annotated_image = np.copy(imageRGB)

    pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
    pose_connections_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)


    for landmarks in pose_landmarks_list: 
        drawing_utils.draw_landmarks(
            annotated_image, 
            landmarks, 
            vision.PoseLandmarksConnections.POSE_LANDMARKS, 
            pose_landmark_style, 
            pose_connections_style)
    return annotated_image


def kick_analyzer(imageRGB, detected_result):
    if detected_result.pose_landmarks:

        imageRGB = imageRGB.copy()
        first_person_landmarks = detected_result.pose_landmarks[0]

        left_knee = first_person_landmarks[25]
        right_knee = first_person_landmarks[26]

        right_ankle = first_person_landmarks[27]
        left_ankle = first_person_landmarks[28]

        right_hip = first_person_landmarks[23]
        left_hip = first_person_landmarks[24]

        left_foot = first_person_landmarks[31]
        right_foot = first_person_landmarks[32]

        if right_knee.visibility > 0.5 and right_ankle.visibility > 0.5:
            angle = calculate_angle(right_hip, right_knee, right_ankle)
            if angle > 20 and angle < 100:
                cv.putText(imageRGB, "Preparing Kick Right", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if left_knee.visibility > 0.5 and left_ankle.visibility > 0.5:
            angle = calculate_angle(left_hip, left_knee, left_ankle)
            if angle > 120 and angle < 180:
                cv.putText(imageRGB, "Preparing Kick Left", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if right_ankle.visibility > 0.5 and right_foot.visibility > 0.5:
            angle = calculate_angle(right_ankle, right_foot, right_hip)
            if angle > 90 and angle < 180:
                cv.putText(imageRGB, "Kicking Right", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if left_ankle.visibility > 0.5 and left_foot.visibility > 0.5:
            angle = calculate_angle(left_ankle, left_foot, left_hip)
            if angle > 90 and angle < 180:
                cv.putText(imageRGB, "Kicking Left", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return imageRGB