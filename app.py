from flask import Flask, render_template, Response, jsonify, url_for
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
    # Face detection section
    # Set the facial detection algorithm
    casc_path_face = "haarcascase_frontalface_alt2.xml"
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + casc_path_face)
    data = pickle.loads(open("face_enc", "rb").read())

    # Get the encoding for 
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encoding = face_recognition.face_encodings(rgb)[0]

    # Finding the match
    matches = face_recognition.compare_faces(data["encodings"], encoding)
    name = "Unknown"
    if True in matches:
        matched_index = matches.index(True)
        name = data["names"][matched_index]

    emotion = "sad"

    # From name and emotion, gather a list of songs
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

if __name__ == "main":
    app.run(debug=True)