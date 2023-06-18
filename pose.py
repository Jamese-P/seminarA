import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

src=cv2.imread('bomb.png',-1)
width_bomb, height_bomb = src.shape[:2]
#mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
#mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
#mask = mask / 255  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
#src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。
 
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
    rec2=(500,300)
    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #(1280,720)
    x_left=(results.pose_landmarks.landmark[19].x)*width
    y_left=results.pose_landmarks.landmark[19].y*height
    x_right=results.pose_landmarks.landmark[20].x*width
    y_right=results.pose_landmarks.landmark[20].y*height
    #print(width,height,x_left,y_left,x_right,y_right)

    if (rec1[0]<x_left) and (rec2[0]>x_left) and(rec1[1]<y_left) and (rec2[1]>y_left):
      print("left touch")
      #image[100:height_bomb+100,200:width_bomb+200]=src
      #cv2.imwrite('out.jpg',image)
    if (rec1[0]<x_right) and (rec2[0]>x_right) and(rec1[1]<y_right) and (rec2[1]>y_right):
      print("right touch")
 
    #図形を描画
    cv2.rectangle(image, rec1,rec2, (0, 255, 0), thickness=8)

    # 検出されたポーズの骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    #cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()