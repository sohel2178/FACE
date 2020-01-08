import face_recognition
import cv2
import numpy as np
import os
import ntpath

import codecs, json

import pickle

from matplotlib import pyplot as plt

# np.load('images.pickle').shape

# with open('images.pickle','rb') as f:
#     x = pickle.load(f)
#     first = x[0]
#     print(first)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

known_encodings = []
known_labels = []

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            print(path)
            face = face_recognition.load_image_file(path)
            try:
                face_encoding = face_recognition.face_encodings(face)[0]
                known_encodings.append(face_encoding)
                known_labels.append(ntpath.basename(path).split(".")[0])
                # print(type(face_encoding))
                # print(ntpath.basename(path).split(".")[0])
            except:
                print("Wrong Thing Happen")


print(len(known_encodings),"Encoding Size")
print(len(known_labels),"Labels Size")

with open("images.pickle",'wb') as f:
    pickle.dump(known_encodings,f)

with open("labels.pickle","wb") as f:
    pickle.dump(known_labels,f)


# sohel_image = face_recognition.load_image_file("sohel.jpg")
# sohel_face_encoding = face_recognition.face_encodings(sohel_image)[0]

# print(sohel_face_encoding)

# redwan_image = face_recognition.load_image_file("redwan.jpg")
# redwan_face_encoding = face_recognition.face_encodings(redwan_image)[0]

# imran_image = face_recognition.load_image_file("imran.jpg")
# imran_image_encoding = face_recognition.face_encodings(imran_image)[0]

# smith_image = face_recognition.load_image_file("smith.jpg")
# smith_face_encoding = face_recognition.face_encodings(smith_image)[0]

# cap = cv2.VideoCapture('http://192.168.1.20:4747/mjpegfeed?640x480')


# process_this_frame = True

# known_face_encodings = [
#     sohel_face_encoding,
#     redwan_face_encoding,
#     imran_image_encoding,
#     smith_face_encoding
# ]

# face_labels = ["Sohel Ahmed","Redwan Moin","Imran Hasan","Smith"]


# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Resize frame of video to 1/4 size for faster face recognition processing
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     rgb_small_frame = small_frame[:, :, ::-1]

#     if process_this_frame:
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#         # print(face_encodings)

#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

#             best_match_index = np.argmin(face_distances)

#             print(matches)

#             name = face_labels[best_match_index]

#             for (top, right, bottom, left) in face_locations:
#                 top *= 4
#                 right *= 4
#                 bottom *= 4
#                 left *= 4

#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#                 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX

#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#     # print(rgb_small_frame)

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



