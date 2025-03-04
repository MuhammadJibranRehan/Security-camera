import cv2
import os
import time
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

# Create a directory for storing recordings
if not os.path.exists("recordings"):
    os.makedirs("recordings")

# Initialize camera
camera = cv2.VideoCapture(0)
recording = False
video_writer = None
recording_filename = ""

def generate_frames():
    """Stream live camera feed."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if recording and video_writer is not None:
                video_writer.write(frame)  # Save frame to video file

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Provide live video stream."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    """Start recording the video."""
    global recording, video_writer, recording_filename

    if recording:
        return jsonify({"message": "Already recording!"})

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    recording_filename = f"recordings/recording_{timestamp}.mp4"
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    video_writer = cv2.VideoWriter(recording_filename, fourcc, 20.0, (frame_width, frame_height))

    recording = True
    return jsonify({"message": "Recording started!"})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    """Stop recording and save the file."""
    global recording, video_writer

    if not recording:
        return jsonify({"message": "No recording in progress!"})

    recording = False
    video_writer.release()
    video_writer = None

    return jsonify({"message": f"Recording saved as {recording_filename}"})

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handle file uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    save_path = os.path.join("recordings", file.filename)
    file.save(save_path)
    
    return jsonify({"message": f"File uploaded successfully as {save_path}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
