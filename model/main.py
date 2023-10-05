# gaze_estimation_dataset.py
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image

from data import DataSet
import train_fine_tune_data as fineTune

data = Dataset('./')
data.load_landmarks_from_csv()
data.load_gaze_from_csv()
data.load_frame_from_csv()

def __init__(self):
    self.data_paths = data_paths
    self.landmark_data = landmark_data
    self.gaze_coordinates = gaze_coordinates
    self.transform = transform

def __len__(self):
    return len(self.data_paths)

def __getitem__(self, idx):
    image = transforms.ToTensor()(Image.open(self.data_paths[idx]))
    landmarks = self.landmark_data[idx]
    gaze_coordinates = self.gaze_coordinates[idx]

    if self.transform:
        image = self.transform(image)

    return image, landmarks, gaze_coordinates

def fine_tune_frames(self):
    train_fine_tune_data.fine_tune_vit_model(image_paths, landmark_data, gaze_coordinates)