from flask import Flask, render_template, Response, request
import cv2
from VideoProcessor import VideoProcessor
from landmark_extraction import LandmarkFinder


import subprocess
# Define the wget command as a list of arguments
wget_command = [
    'wget',
    '-O', 'face_landmarker_v2_with_blendshapes.task',  # Output filename
    'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'
]

# Execute the wget command
try:
    subprocess.run(wget_command, check=True)
    print("Download completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Download failed with error: {e}")
    
import logging
# Configure the logging system
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('my_app.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/static')
video_stream = cv2.VideoCapture(0)  # Open default camera (index 0)
video_processor = VideoProcessor(video_stream)

@app.route('/')
def camera_permission():
    return render_template('eye_tracker.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_processor.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_image', methods=['POST'])
def save_image():
    frame_data = request.json['image_data']
    frame = video_processor.save_frame(frame_data)
    
    # Process the captured image data here
    # change the format
    landmarks = LandmarkFinder.extract_landmarks(frame)
    logger.info("Done.")

    return 'Image data received'

if __name__ == '__main__':
    app.run(debug=True)


