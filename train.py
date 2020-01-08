import cv2
import os
import numpy as np
from PIL import Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

face_casecade = cv2.CascadeClassifier('casecade/data/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

label_ids = {}
current_id = 0

image_list = []

x_train = []
y_labels = []

counter = 0

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            
            if not label in label_ids:
                label_ids[label] = current_id
                current_id+=1

            id_ = label_ids[label]

            pil_image = Image.open(path).convert("L")
            size = (220,220)
            final_image = pil_image.resize(size,Image.ANTIALIAS)
            image_arr = np.array(final_image,"uint8")

            faces = face_casecade.detectMultiScale(image_arr, scaleFactor=1.1, minNeighbors=3)

            for (x,y,w,h) in faces:
                roi = image_arr[y:y+h,x:x+w]
                res = cv2.resize(roi, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
                # s= (100,100)
                # bb = roi.resize(s,Image.ANTIALIAS)
                # cc = np.array(bb,"uint8")
                cv2.imwrite("./tempimages/"+str(id_)+"-"+str(counter)+".jpg",res)
                counter+=1
                x_train.append(res)
                y_labels.append(id_)


with open("pickles/face-labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)


with open("pickles/face-labels.pickle", 'rb') as f:
    print(pickle.load(f))

recognizer.train(x_train, np.array(y_labels))
recognizer.save("recognizers/face-trainner.yml")

print(y_labels)