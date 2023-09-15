from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import cv2


def get_specific_landmarks(rgb_image, detection_result, selected_indexes):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)
  print(annotated_image.shape)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]
    selected_face_landmarks = []
    for i in selected_indexes:
      selected_face_landmarks.append(face_landmarks[i])
    return selected_face_landmarks


def circle_specific_landmarks(rgb_image, detection_result, selected_indexes, img):
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