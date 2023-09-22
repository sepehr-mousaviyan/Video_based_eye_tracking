# train_combined_gaze_model.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from multi_modal_gaze_model import MultiModalGazeModel
from gaze_estimation_dataset import GazeEstimationDataset
from facial_landmark_model import FacialLandmarkModel

def train_combined_gaze_model(image_paths, landmark_data, gaze_coordinates, num_epochs=10, lr=0.001):
    landmark_model = FacialLandmarkModel(num_output_units)
    landmark_model.load_state_dict(torch.load('path_to_pretrained_landmark_model.pth'))

    model_vit = ViT('B_16_imagenet1k', pretrained=True)

    num_output_units = 2
    model = MultiModalGazeModel(model_vit, landmark_model, num_output_units)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    train_dataset = GazeEstimationDataset(image_paths, landmark_data, gaze_coordinates)
    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    model.train()
    for epoch in range(num_epochs):
        for batch_idx, (images, landmarks, gaze_coordinates) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(images, landmarks)
            loss = criterion(outputs, gaze_coordinates)
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), 'combined_gaze_model.pth')
