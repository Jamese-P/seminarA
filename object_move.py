import cv2
import random
import math

# Webカメラから入力
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
out = cv2.VideoWriter('output/sample.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 15, (int(width), int(height)))

fore=(50,50)

speed=20.0 #1回の画面で動くピクセルすう
angle=math.pi/3

rec1=(random.randint(1,width-100),random.randint(1,height-100))
rec2=(rec1[0]+fore[0],rec1[1]+fore[1])
pre=rec1

while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    #out.write(image)

    rec1=(int(pre[0]+speed*math.cos(angle)),int(pre[1]+speed*math.sin(angle)))
    rec2=(rec1[0]+fore[0],rec1[1]+fore[1])

    if rec1[0]+fore[0]>width or rec1[0]<0:
       angle=math.pi-angle
    if rec1[1]+fore[1]>height or rec1[1]<0:
       angle=-1*angle
    pre=rec1


    cv2.rectangle(image, rec1,rec2, (0, 255, 0), thickness=4)

    

    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

#out.release()
cap.release()