# gaze_estimation_dataset.py
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image

class GazeEstimationDataset(Dataset):
    def __init__(self, data_paths, landmark_data, gaze_coordinates, transform=None):
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
