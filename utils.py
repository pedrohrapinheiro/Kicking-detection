import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import cv2 as cv

text = ""
text_left = ""
text_right = ""
kicking_left = False
kicking_right = False

def calculate_angle(a, b, c):
    radians = np.arctan2(c.y - b.y, c.x - b.x) - np.arctan2(a.y - b.y, a.x - b.x)
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

def kick_state(hip, knee, ankle, kicking, previous_angle=None):
    angle = calculate_angle(hip, knee, ankle)
    global text
    if previous_angle is not None:

        # Leg is extending
        if angle < 30:
            text = "Kicking"
            kicking = True

        # Leg is retracting
        elif kicking and angle > previous_angle:
            text = "Finishing Kick"

        # Back to chamber position
        elif 30 < angle < 60 and not kicking:
            text = "Preparing Kick"

        # Leg is almost straight again
        elif kicking and angle > 90:
            text = "Finished Kick"
            kicking = False

    previous_angle = angle

    return text, kicking, previous_angle
     

def kick_analyzer(imageRGB, detected_result, previous_angle_left, previous_angle_right):
    global text_left
    global text_right
    global kicking_left
    global kicking_right
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
        if right_knee.visibility > 0.3 and right_foot.visibility > 0.3:
            text_right, kicking_right, previous_angle_right = kick_state(right_hip, right_knee, right_ankle, kicking_right, previous_angle_right)
            
        if left_knee.visibility > 0.3 and left_ankle.visibility > 0.3:
            text_left, kicking_left, previous_angle_left = kick_state(left_hip, left_knee, left_ankle, kicking_left, previous_angle_left)
        
        if text_left != "":
            cv.putText(
                imageRGB,
                text_left,
                (20, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )
        
        if text_right != "":
            cv.putText(
                imageRGB,
                text_right,
                (imageRGB.shape[1] - 300, 50),
                cv.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

        
        cv.putText(imageRGB, f'right_hip_X: {right_hip.x:.2f}, right_hip_Y: {right_hip.y:.2f}', (20, 100), cv.FONT_HERSHEY_SIMPLEX,   0.4, (0, 0, 255), 2)
        cv.putText(imageRGB, f'right_knee_X: {right_knee.x:2f}, right_knee_Y: {right_knee.y:.2f}', (20, 150), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
        cv.putText(imageRGB, f'right_foot_X: {right_ankle.x:.2f}, right_ankle_Y: {right_ankle.y:.2f}', (20, 200), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
        cv.putText(imageRGB, f"angle: {calculate_angle(right_hip, right_knee, right_ankle)}", (20, 250), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

        cv.putText(imageRGB, f'left_hip_X: {left_hip.x:.2f}, left_hip_Y: {left_hip.y:.2f}', (20, 300), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        cv.putText(imageRGB, f'left_knee_X: {left_knee.x:.2f}, left_knee_Y: {left_knee.y:.2f}', (20, 350), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        cv.putText(imageRGB, f'left_ankle_X: {left_ankle.x:.2f}, left_ankle_Y: {left_ankle.y:.2f}', (20, 400), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        cv.putText(imageRGB, f"angle: {calculate_angle(left_hip, left_knee, left_ankle)}", (20, 450), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
    
    #Note to self:
    #Calcular quando ela tiver estendida -> chute
    #Calcula quando ela tiver se estendendo -> quase chutando -> intervalo de valores, se tiver dentro desses valores ta estendendo
    #Calcular volta -> finished kicking return to preparing kick
    #Pe no chao -> finished kick
    return imageRGB, previous_angle_left, previous_angle_right