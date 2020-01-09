import face_recognition
import cv2
import numpy as np
import pickle
import client


known_encodings = []
known_labels = []


with open('images.pickle','rb') as f:
    known_encodings = pickle.load(f)

with open('labels.pickle','rb') as f:
    known_labels = pickle.load(f)


cap = cv2.VideoCapture('http://192.168.1.25:4747/mjpegfeed?640x480')

process_this_frame = True


name_list = []


def all_same(l):
    return all(x == l[0] for x in l)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # frame = cv2.UMat(frame)

    # print(type(bb))

    if ret:

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # print(small_frame.shape)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]




        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # print(face_encodings)

            for face_encoding in face_encodings:
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)

                if min(face_distances) <=0.35:

                    best_match_index = np.argmin(face_distances)
                    name = known_labels[best_match_index]
                    name = name.split('-')[0]

                    for (top, right, bottom, left) in face_locations:
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX

                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                        name_list.append(name)

                        if len(name_list)>=8:
                            if all_same(name_list[-8:]):
                                print("Found Face")
                                client.send_message(b"UNLOCK")
                                name_list=[]

        # print(rgb_small_frame)

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('Face Detector',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()