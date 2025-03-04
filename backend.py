from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Folder to store recorded videos
RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

# Start recording (Dummy Response - Implement actual recording logic)
@app.route("/start_record", methods=["POST"])
def start_record():
    return jsonify({"message": "Recording started!"}), 200

# Stop recording (Dummy Response - Implement actual stop logic)
@app.route("/stop_record", methods=["POST"])
def stop_record():
    return jsonify({"message": "Recording stopped!"}), 200

# Upload video file
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    filepath = os.path.join(RECORDINGS_FOLDER, filename)
    file.save(filepath)

    return jsonify({"message": f"File {filename} uploaded successfully!"}), 200

# Serve last recorded video
@app.route("/get_last_video")
def get_last_video():
    files = sorted(os.listdir(RECORDINGS_FOLDER), reverse=True)
    if files:
        return send_from_directory(RECORDINGS_FOLDER, files[0])
    return jsonify({"error": "No recorded videos found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
