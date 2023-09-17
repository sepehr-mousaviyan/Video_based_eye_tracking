import cv2
import os
import Util as util
from landmark_extraction import LandmarkFinder

class VideoProcessor:
    def __init__(self, video_stream):
        self.video_stream = video_stream
        # Folder path to save the frames
        self.frame_save_path = './frames/'
        self.frame_count = 0
        
    def circle_image(self, frame, landmarks):
        output_frame = LandmarkFinder.circle_specific_landmarks(frame, landmarks)
        return output_frame
    
    def process_frame(self, frame):
        landmarks = LandmarkFinder.extract_landmarks(frame)
        return landmarks, self.circle_image(frame, landmarks)
        
    
    
    def generate_frames(self):
        frame_count = 0
        while True:
            success, frame = self.video_stream.read()
            if not success:
                break

            processed_frame = self.process_frame(frame)

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()

            # Yield the frame as a response to the client
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            frame_count += 1



    def save_frame(self, frame_data):
        # Create the directory if it doesn't exist
        os.makedirs(self.frame_save_path, exist_ok=True)
        filename = f'frame_{self.frame_count}.jpg'
        file_path = os.path.join(self.frame_save_path, filename)
        util.save_base64_image(frame_data, file_path)
        self.frame_count = self.frame_count + 1
        saved_image = cv2.imread(file_path)
        return saved_image
        