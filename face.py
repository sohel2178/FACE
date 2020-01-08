import numpy as np
import cv2
import pickle

face_casecade = cv2.CascadeClassifier('casecade/data/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture('http://192.168.1.13:4747/mjpegfeed?640x480')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {}

with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

print(labels)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_casecade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    for (x,y,w,h) in faces:
        # print(x,y,w,h)

        roi_gray = gray[y:y+h, x:x+w]

        res = cv2.resize(roi_gray, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)

        id_, conf = recognizer.predict(res)

        cv2.imwrite('a.jpg',roi_gray)

        # img_item = "7.png"
    	# cv2.imwrite(img_item, roi_gray)

        if conf<=99:
            print(id_,conf)


        color = (255, 0, 0) #BGR 0-255
        stroke = 2
        cv2.rectangle(frame,(x,y),(x+w,y+h),color,stroke)
    	# stroke = 2
    	# end_cord_x = x + w
    	# end_cord_y = y + h
    	# cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()