import cv2
import random
import time

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

while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False

    out.write(image)

    if (time.time()-time_pre)>5:
      rec1=(random.randint(1,width-100),random.randint(1,height-100))
      rec2=(rec1[0]+100,rec1[1]+100)
      time_pre=time.time()
      f.write(str(rec1))

    #図形を描画
    cv2.rectangle(image, rec1,rec2, (0, 255, 0), thickness=8)

    cv2.imshow('image',image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

    if (time.time()-time_sta)>30:
        print("finish record")
        break
out.release()
cap.release()
f.close()
