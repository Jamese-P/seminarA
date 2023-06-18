import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
 
# Webカメラから入力
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    rec1=(50,80)
    rec2=(125,130)
    x_left=results.pose_landmarks.landmark[19].x
    y_left=results.pose_landmarks.landmark[19].y
    x_right=results.pose_landmarks.landmark[20].x
    y_right=results.pose_landmarks.landmark[20].y
 
    # 検出されたポーズの骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    cv2.rectangle(image, rec1,rec2, (0, 255, 0), thickness=-1)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()