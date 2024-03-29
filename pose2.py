import cv2
import mediapipe as mp
import random
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# Webカメラから入力
cap = cv2.VideoCapture(1)
fps = cap.get(cv2.CAP_PROP_FPS)
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
out = cv2.VideoWriter('output/sample.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 15, (int(width), int(height)))

f=open('output/coordinate.txt','w')

rec1=(random.randint(1,width-100),random.randint(1,height-100))
rec2=(rec1[0]+100,rec1[1]+100)

time_sta=time.time()
time_pre=time.time()

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False

    out.write(image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

 
    if (time.time()-time_pre)>5:
      rec1=(random.randint(1,width-100),random.randint(1,height-100))
      rec2=(rec1[0]+100,rec1[1]+100)
      time_pre=time.time()
      f.write(str(rec1))

    

    #図形を描画
    cv2.rectangle(image, rec1,rec2, (0, 255, 0), thickness=8)

    #out.write(image)

    #(1280,720)
    x_left=results.pose_landmarks.landmark[19].x*width
    y_left=results.pose_landmarks.landmark[19].y*height
    x_right=results.pose_landmarks.landmark[20].x*width
    y_right=results.pose_landmarks.landmark[20].y*height
    #print(width,height,x_left,y_left,x_right,y_right)
    image.flags.writeable = True
    
    
    # 検出されたポーズの骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    image=cv2.flip(image,1)
    
    # 衝突検出
    if (rec1[0]<x_left) and (rec2[0]>x_left) and(rec1[1]<y_left) and (rec2[1]>y_left):
      #print("left touch")
      cv2.putText(image, 'left touch', (int(width-x_left),int(y_left)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    if (rec1[0]<x_right) and (rec2[0]>x_right) and(rec1[1]<y_right) and (rec2[1]>y_right):
      #print("right touch")
      cv2.putText(image, 'right touch', (int(width-x_right),int(y_right)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)

    #out.write(image)
    #cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break
    
    if (time.time()-time_sta)>30:
      print("finish record")
      break
out.release()
cap.release()
f.close()