from flask import Flask, render_template, Response, jsonify, url_for
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
import os
import numpy as np
import cv2
import sqlite3
import random
import face_recognition
import time
import pickle
import imutils

app = Flask(__name__)

# Configure GPUs is available
gpus = tf.config.list_physical_devices("GPU")
try:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
except:
    pass

# Connect camera to the application
camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/predict')
def predict_playlist():
    """ Face detection section """
    # Load emotion detection model
    classifier = load_model("emotion_detection.h5")

    # Set the facial detection algorithm
    casc_path_face = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(casc_path_face)
    data = pickle.loads(open("face_enc", "rb").read())

    # Preprocess the face
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    try:
        encoding = face_recognition.face_encodings(rgb)[0]
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            raise Exception
    except IndexError:
        error_message = "There is no face detected on the camera. Please try again."
        return render_template("predict_error.html", error_message=error_message)
    except Exception:
        error_message = "The system can't properly detect your emotion. Please adjust light and angles of the face."
        return render_template("predict_error.html", error_message=error_message)

    # Classify the emotion
    class_labels = ['angry', 'happy', 'neutral', 'sad', 'surprised']
    for x, y, w, h in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = classifier.predict(roi)[0]
            emotion = class_labels[preds.argmax()]

    # Finding the match
    matches = face_recognition.compare_faces(data["encodings"], encoding)
    name = "Unknown"
    if True in matches:
        matched_index = matches.index(True)
        name = data["names"][matched_index]

    # From name and emotion, gather a list of songs
    if name != "Unknown":
        conn = sqlite3.connect(os.path.join(os.getcwd(), "database.db"))
        curr = conn.cursor()
        curr.execute(
            """
            SELECT transactions.song_link
            FROM transactions
            INNER JOIN users ON users.user_id = transactions.user_id
            INNER JOIN emotions ON emotions.emotion_id = transactions.emotion_id
            WHERE emotions.emotion=? AND users.first_name=?
            """,
            (emotion, name)
        )
        song_list = curr.fetchall()
        songs = [song[0] for song in song_list]
        songs = random.sample(songs, 5)

        return render_template("predict.html", name=name, emotion=emotion, songs=songs)
    else:
        conn = sqlite3.connect(os.path.join(os.getcwd(), "database.db"))
        curr = conn.cursor()
        curr.execute(
            """
            SELECT transactions.song_link
            FROM transactions
            INNER JOIN emotions ON emotions.emotion_id = transactions.emotion_id
            WHERE emotions.emotion=?
            """,
            (emotion,)
        )
        song_list = curr.fetchall()
        songs = [song[0] for song in song_list]
        songs = random.sample(songs, 5)
        
        return render_template("predict_unknown.html", songs=songs, emotion=emotion)


if __name__ == "main":
    app.run(debug=True)
