from flask import Flask, render_template, Response, jsonify
import os
import numpy as np 
import cv2
import json

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
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/predict')
def predict_playlist():
    success, frame = camera.read()
    # TODO
    # Preprocess the frame

    # TODO
    # Predict the person and emotion

    # TODO
    # Create a JSON to send back to front end
    pass

if __name__ == "main":
    app.run(debug=True)