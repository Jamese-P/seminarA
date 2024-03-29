import cv2
import mediapipe as mp
import numpy as np
import math
from scipy.spatial import distance
import time
import argparse
import pandas as pd
import random
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
angle = 0
 
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

  if straight_finger==5:
    #print("paa")
    return 1
  elif straight_finger==1 or straight_finger==0:
   # print("guu")
    return 2
  
  return -1

def comp(fore_img, image, dx,dy):
      h, w = fore_img.shape[:2]
      fore_x_min, fore_x_max = 0, w
      fore_y_min, fore_y_max = 0, h
 
      back_h, back_w = image.shape[:2]
      back_x_min, back_x_max = dx, dx+w
      back_y_min, back_y_max = dy, dy+h
      
      if back_x_min < 0:
          fore_x_min = fore_x_min - back_x_min
          back_x_min = 0
         
      if back_x_max > back_w:
          fore_x_max = fore_x_max - (back_x_max - back_w)
          back_x_max = back_w
 
      if back_y_min < 0:
          fore_y_min = fore_y_min - back_y_min
          back_y_min = 0
         
      if back_y_max > back_h:
          fore_y_max = fore_y_max - (back_y_max - back_h)
          back_y_max = back_h
      
      #大きさを取得して画像内に入るように大きさを制限

      roi = image[back_y_min:back_y_max, back_x_min:back_x_max]
      sync_img = fore_img[fore_y_min:fore_y_max, fore_x_min:fore_x_max]
      if(fore_x_max>fore_x_min and fore_y_max > fore_y_min):
        img2gray = cv2.cvtColor(sync_img,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        img2_fg = cv2.bitwise_and(sync_img,sync_img,mask = mask)
        dst = cv2.add(img1_bg,img2_fg)
        image[back_y_min:back_y_max, back_x_min:back_x_max] = dst
          
      return image

def move_obj(fore_image,x,y,v):
   vx = 0
   vy = 0
   #if(hands == 'guu'):
   #x,y = parabolic(x,y,v,vx,vy)

   #elif(hands == 'paa'):
     # None
   

def touch_judge(hand_x,hand_y,dx,dy,fore_img,image):
      h, w = fore_img.shape[:2]
 
      back_h, back_w = image.shape[:2]
      back_x_min, back_x_max = dx, dx+w
      back_y_min, back_y_max = dy, dy+h
      
      if(back_x_min<hand_x and hand_x < back_x_max and back_y_min < hand_y and hand_y < back_y_max):
         return True
      else:
         return False

#TODO
def in_rect(image,pose_landmark,target):
    #ここで11,12,23,24の座標がほしい->エラーはく
    h,w=image.shape[:2]
    a = (pose_landmark[11].x*w, pose_landmark[11].y*h)
    b = (pose_landmark[12].x*w, pose_landmark[12].y*h)
    c = (pose_landmark[23].x*w, pose_landmark[23].y*h)
    d = (pose_landmark[24].x*w, pose_landmark[24].y*h)
    e = (target[0], target[1])

    # 原点から点へのベクトルを求める
    vector_a = np.array(a)
    vector_b = np.array(b)
    vector_c = np.array(c)
    vector_d = np.array(d)
    vector_e = np.array(e)

    # 点から点へのベクトルを求める
    vector_ab = vector_b - vector_a
    vector_ae = vector_e - vector_a
    vector_bc = vector_c - vector_b
    vector_be = vector_e - vector_b
    vector_cd = vector_d - vector_c
    vector_ce = vector_e - vector_c
    vector_da = vector_a - vector_d
    vector_de = vector_e - vector_d

    # 外積を求める
    vector_cross_ab_ae = np.cross(vector_ab, vector_ae)
    vector_cross_bc_be = np.cross(vector_bc, vector_be)
    vector_cross_cd_ce = np.cross(vector_cd, vector_ce)
    vector_cross_da_de = np.cross(vector_da, vector_de)

    result=(vector_cross_ab_ae < 0 and vector_cross_bc_be < 0 and vector_cross_cd_ce < 0 and vector_cross_da_de < 0)
    if result:
      print(result)
    return result
      
def reflect(angle,fore_img, image, dx,dy):
  global reflect_flag
  global obj_vec
  h, w = fore_img.shape[:2]

  back_h, back_w = image.shape[:2]
  back_x_min, back_x_max = dx, dx+w
  back_y_min, back_y_max = dy, dy+h
  
  if back_x_min < 0 or back_x_max > back_w:
      angle=180-angle
      reflect_flag = True
      obj_vec=obj_vec+10

  if back_y_min < 0 or back_y_max > back_h:
      angle=-1*angle
      reflect_flag = True
      obj_vec=obj_vec+10

  return angle

#TODO
def show_goal(image,goal1,goal2):
   h, w = image.shape[:2]
   cv2.line(image,(10,int(goal1)),(10,int(goal1+150)),color=(0, 255, 0),thickness=3,lineType=cv2.LINE_4,shift=0)
   cv2.line(image,(w-10,int(goal2)),(w-10, int(goal2+150)),color=(0, 255, 0),thickness=3,lineType=cv2.LINE_4,shift=0)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--video_path', type=str, default='', help='Path to the video file.')
args = parser.parse_args()
if args.video_path != '':
  cap = cv2.VideoCapture(args.video_path)
else:
  cap = cv2.VideoCapture(1)

width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

px=random.randint(1,width-100)
py=random.randint(1,height-100)

obj_touched = False
obj_touch_now = False
hand_velocity = 0
#TODO
obj_vec=100
previous_hands_pos = [0,0]
now_hands_pos = [0,0] 
previous_hand_time = 0
now_hand_time = 0
dist = 0
reflect_flag = True

#TODO
goal1=random.randint(1,height-100)
goal2=random.randint(1,height-100)
flag_goal1=1
flag_goal2=-1

count = 0

nowtime = 0
pasttime = 0

fore_img = cv2.imread(r"data/ball.png")
fore_img = cv2.resize(fore_img, (100, 100))
start_time = time.perf_counter()
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        break
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      pose_results = pose.process(image)
      hands_results = hands.process(image)

      #計測フレーム数を増加
      count +=1
      pasttime = nowtime
      nowtime = time.perf_counter()
 
      # 検出されたポーズの骨格をカメラ画像に重ねて描画
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if hands_results.multi_hand_landmarks:
        x=hands_results.multi_hand_landmarks[0].landmark[9].x
        y=hands_results.multi_hand_landmarks[0].landmark[9].y
        height, weight = image.shape[:2]
        previous_hands_pos = now_hands_pos
        now_hands_pos = [x*weight,y*height]
        previous_hand_time = now_hand_time
        now_hand_time = nowtime
        duration = now_hand_time - previous_hand_time

        for hand_landmarks in hands_results.multi_hand_landmarks:
          for hand_landmark in hand_landmarks.landmark:
            if(touch_judge(hand_landmark.x*weight,hand_landmark.y*height,int(px),int(py),fore_img,image)):
              obj_touched = True
              obj_touch_now = True
        
        for hand_landmarks in hands_results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
        
      mp_drawing.draw_landmarks(
          image,
          pose_results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

      #TODO ゴールの描画
      show_goal(image,goal1,goal2)

      if(flag_goal1==-1):
         goal1=goal1-10
      else:
         goal1=goal1+10

      if(flag_goal2==-1):
         goal2=goal2-10
      else:
         goal2=goal2+10

      if(goal1>height-150 or goal1<0):
        flag_goal1=flag_goal1*(-1)
      if(goal2>height-150 or goal2<0):
        flag_goal2=flag_goal2*(-1)

      if(obj_touched):
        if(obj_touch_now and reflect_flag):
          reflect_flag = False
          dist = distance.euclidean(previous_hands_pos, now_hands_pos)
          hand_velocity = dist/duration
          #TODO
          # 削除　obj_vec = hand_velocity
          # ラジアン単位を取得
          radian = -1*math.atan2(previous_hands_pos[1] - now_hands_pos[1], now_hands_pos[0] - previous_hands_pos[0] )
          # ラジアン単位から角度を取得
          angle = radian * (180 / math.pi)
          #print(hand_velocity)
        #x,y = move_img()
        #画像の位置変更
        angle = reflect(angle,fore_img, image, int(px),int(py))
          
        vx = obj_vec*math.cos(angle*math.pi/180.0)
        vy = obj_vec*math.sin(angle*math.pi/180.0)
        px = px+vx*(nowtime - pasttime)
        py = py+vy*(nowtime - pasttime)
      
      #TODO 跳ね返り後の速度変更
      #if(reflect_flag):
       # obj_vec=obj_vec+10
      
      #print(pose_results.pose_landmarks)
      if(pose_results.pose_landmarks):
        in_rect(image,pose_results.pose_landmarks.landmark,(px,py))
      
      cv2.putText(image,'ball',(int(px),int(py)),cv2.FONT_HERSHEY_SIMPLEX,1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)

      #TODO 得点　ボールの速度の表示
      cv2.putText(image,str(obj_vec),(100,100),cv2.FONT_HERSHEY_SIMPLEX,1.0,color=(0, 255, 0),thickness=2,lineType=cv2.LINE_4)

      image = comp(fore_img,image,int(px),int(py))
      obj_touch_now = False
      cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
      if(nowtime -start_time > 200.0):
         print("Frame is")
         print(count/(nowtime -start_time))
         break
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()