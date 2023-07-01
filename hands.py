import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def identify_hand(landmark):
  landmark_x=list()
  landmark_y=list()
  for i in range(21):
    landmark_x.append(landmark[i].x)
    landmark_y.append(landmark[i].y)
  
  fingers=list() #親指、人差し指、中指、薬指、小指
  straight_finger=0

  for i in range(5):
    x=np.array(landmark_x[4*i+1:4*(i+1)])
    y=np.array(landmark_y[4*i+1:4*(i+1)])
    coef=np.corrcoef(x,y)
    fingers.append(abs(coef[0][1]))
    if (abs(coef[0][1])>0.9):
      straight_finger+=1

  #print(straight_finger)

  if straight_finger==5:
    print("paa")
    return 1
  elif straight_finger==1 or straight_finger==0:
    print("guu")
    return 2
  
  return -1

# Webカメラから入力
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
 
    # 検出された手の骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
      height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

      identify_hand(results.multi_hand_landmarks[0].landmark)

      landmark_x=list()
      landmark_y=list()
      for i in range(21):
        x=results.multi_hand_landmarks[0].landmark[i].x*width
        y=results.multi_hand_landmarks[0].landmark[i].y*height
        landmark_x.append(x)
        landmark_y.append(y)

      #print(results.multi_handedness)

      #print(x,y)
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        cv2.drawMarker(image,(100,100),(0,0,0),markerType=cv2.MARKER_STAR, markerSize=10)
    #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()