from imutils import paths
import face_recognition
import pickle
import cv2
import os

image_paths = list(paths.list_images('images'))
known_encodings = []
known_names = []

for i, image_path in enumerate(image_paths):
    name = image_path.split(os.path.sep)[-1].strip(".jpg")
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings:
        known_encodings.append(encoding)
        known_names.append(name)

data = {
    "encodings": known_encodings,
    "names": known_names
}

with open("face_enc", "wb") as f:
    f.write(pickle.dumps(data))
