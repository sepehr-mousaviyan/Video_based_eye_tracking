from flask import Flask, render_template, Response, request, jsonify
import cv2
from VideoProcessor import VideoProcessor
from landmark_extraction import LandmarkFinder
# from properties.ApplicationProperties import ApplicationProperties
# from Logging import configure_logging
import base64


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
    # processed_frame = video_processor.process_frame(frame)
    
    # Process the captured image data here
    # change the format
    
    _, jpeg_image = cv2.imencode('.jpg', frame)
    jpeg_image_data = jpeg_image.tobytes()

    # Encode the JPEG image data as base64
    base64_image_data = base64.b64encode(jpeg_image_data).decode('utf-8')

    # Create a response with the base64-encoded image data
    response = jsonify(image_data=base64_image_data)

    logger.info("Done.")

    return response

if __name__ == '__main__':
    # configure_logging()  # Call the logging configuration function
    app.run(debug=True)


