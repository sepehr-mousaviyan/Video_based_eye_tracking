from flask import Flask, render_template, Response, request
import cv2
from VideoProcessor import VideoProcessor

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
    video_processor.save_frame(frame_data)
    
    # Process the captured image data here
    # ...

    return 'Image data received'

if __name__ == '__main__':
    app.run(debug=True)


