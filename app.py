from flask import Flask, render_template, Response, jsonify, url_for
import os
import numpy as np 
import cv2
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.py")
curr = conn.cursor()

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
    # TODO
    # Preprocess the frame

    # TODO
    # Predict the person and emotion
    name = "jed"
    emotion = "happy"
    cwd = os.getcwd()
    # path = os.path.join(cwd, "templates", "music", "jed", "emotion")
    # song_list = os.listdir(path)

    # Create a JSON of name, emotion, and songs to play
    # data = {
    #     "user": name,
    #     "mood": emotion,
    #     "songs": song_list
    # }

    return render_template("predict.html", name=name, emotion=emotion)

if __name__ == "main":
    app.run(debug=True)