from flask import Flask, Response, request, jsonify
import cv2
import threading
import os
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)

recording = False
video_writer = None
output_folder = "recordings"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, video_writer

    if not recording:
        filename = os.path.join(output_folder, f"recording_{int(time.time())}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 Format
        fps = 20.0
        frame_size = (int(camera.get(3)), int(camera.get(4)))
        video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        recording = True
        return jsonify({"message": "Recording started", "filename": filename})
    else:
        return jsonify({"message": "Already recording"}), 400

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording, video_writer

    if recording:
        recording = False
        video_writer.release()
        return jsonify({"message": "Recording stopped"})
    else:
        return jsonify({"message": "No active recording"}), 400

@app.route('/latest_video', methods=['GET'])
def latest_video():
    files = sorted(os.listdir(output_folder), reverse=True)
    if files:
        return jsonify({"latest_video": os.path.join(output_folder, files[0])})
    else:
        return jsonify({"message": "No recordings found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
