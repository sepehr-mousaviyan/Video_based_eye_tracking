from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

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


landmarks_number = {
    'left_eye_border': [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7],
    'right_eye_border': [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382],
    'face_grid': [10, 338, 297, 332, 284, 251, 389, 356, 454, 366, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109],
    'right_pupil': [473, 474, 475, 476],
    'left_pupil': [468, 469, 470, 471, 472]
}
def get_specific_landmarks(rgb_image, detection_result, selected_indexes):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)
  x, y = rgb_image.shape[0], rgb_image.shape[1]
  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]
    selected_face_landmarks = []
    for i in selected_indexes:
      list = face_landmarks[i]
      # print(type(list))
      # print('ssssssssssssssss')
      # print(type(list.x))
      X = int(np.ceil(y*(list.x)))
      Y = int(np.ceil(x*(list.y)))
      pair = (X, Y)
      selected_face_landmarks.append(pair)
    return selected_face_landmarks

def circle_specific_landmarks(img, landmarks, left_eye_border = True, right_eye_border = True, face_grid = True, right_pupil = True, left_pupil = True):
  target_categories = []
  if (left_eye_border):
    target_categories.append('left_eye_border')
  if (left_eye_border):
    target_categories.append('right_eye_border')
  if (left_eye_border):
    target_categories.append('face_grid')
  if (left_eye_border):
    target_categories.append('right_pupil')
  if (left_eye_border):
    target_categories.append('left_pupil')
    
    
  print(landmarks)
  
  for mark in landmarks:
    if mark['name'] in target_categories:
      landmark_points = mark['landmarks']
      for pair in landmark_points:
        print(pair[0])
        print(pair[1])
        img = cv2.circle(img, (pair[0], pair[1]), radius=0, color=(0, 0, 255), thickness=2)
      # # Iterate through pairs of landmarks within this 'name'
      # for i in range(len(landmark_points) - 1):
      #     for j in range(i + 1, len(landmark_points)):
      #         landmark1 = landmark_points[i]
      #         landmark2 = landmark_points[j]
            
      #       # Print or process the pair of landmarks as needed
      #       print(f"Name: {name}, Landmark Pair: {landmark1}, {landmark2}")
  
  # for category_data in landmarks:
  #   str = category_data['name']
  #   if str in target_categories:
  #     # Found the target category
  #     for landmark_data in category_data.landmarks:
  #        x , y = landmark_data
  #        print(x)
  #       img = cv2.circle(img, (landmark_data['x'], landmark_data['y']), radius=0, color=(0, 0, 255), thickness=20)

  return img

def circle_specific_landmarks_by_index(rgb_image, detection_result, selected_indexes, img):
  selected_face_landmarks = get_specific_landmarks(rgb_image, detection_result, selected_indexes)
  x, y = rgb_image.shape[0], rgb_image.shape[1]
  print(x,y)
  # print(np.ceil(x*landmark[0]))
  i = 1
  for landmark in selected_face_landmarks:
    # print(landmark.x)
    X = int(np.ceil(y*(landmark.x)))
    Y = int(np.ceil(x*(landmark.y)))
    img = cv2.circle(img, (X, Y), radius=0, color=(0, 0, 255), thickness=20)

    img = cv2.putText(img, str(i), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
    i+=1
    # cv2_imshow(img)
  return img


def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()
  
def detection(raw_frame):
  base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
  options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=True,
                                        output_facial_transformation_matrixes=True,
                                        num_faces=1)
  detector = vision.FaceLandmarker.create_from_options(options)

  # frame = mp.Image.create_from_file(frame_path)
  logger.info('first of detect')
  print(type(raw_frame))
  # image = Image.fromarray(raw_frame)
  # print(type(image))
  logger.info('before frame')
  
  # raw_frame = raw_frame.astype(np.float32)
  logger.info('after typoe changing')
  print(type(raw_frame))
  # converted_frame = raw_frame.astype(np.float32)  # You may need to adjust the format

# Create an Image object with the appropriate format
  # image_format = mp.ImageFormat.Format.VEC32F1  # Replace with the correct format
  frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=raw_frame)
  
  # frame = mp.Image(raw_frame)
  logger.info('end of detect')
  print(type(frame))
  
  detection_result = detector.detect(frame)
  logger.info('end of detect')
  return detection_result
def extract_landmarks(frame):
  logger.info('here')
  print(type(frame))
  # cv2.imshow("this",frame)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
  logger.info('there')
  detection_result = detection(frame)
  logger.info('after detection_result')
  # for diffrent parts:
  landmarks = []

  # Get landmarks for left eye border and associate with a name
  left_eye_border_landmarks = {'name': 'left_eye_border', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['left_eye_border'])}

  # Get landmarks for right eye border and associate with a name
  right_eye_border_landmarks = {'name': 'right_eye_border', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['right_eye_border'])}

  # Get landmarks for face grid and associate with a name
  face_grid_landmarks = {'name': 'face_grid', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['face_grid'])}

  # Get landmarks for right pupil and associate with a name
  right_pupil_landmarks = {'name': 'right_pupil', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['right_pupil'])}

  # Get landmarks for left pupil and associate with a name
  left_pupil_landmarks = {'name': 'left_pupil', 'landmarks': get_specific_landmarks(frame, detection_result, landmarks_number['left_pupil'])}

  # Append the dictionaries to the 'landmarks' list
  landmarks.extend([left_eye_border_landmarks, right_eye_border_landmarks, face_grid_landmarks, right_pupil_landmarks, left_pupil_landmarks])

  return landmarks