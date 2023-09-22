# fine_tune_vit.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pytorch_pretrained_vit import ViT
from gaze_estimation_dataset import GazeEstimationDataset

def fine_tune_vit_model(image_paths, landmark_data, gaze_coordinates, num_epochs=10, lr=0.001, save_path='fine_tuned_vit_model.pth'):
    model_vit = ViT('B_16_imagenet1k', pretrained=True)
    criterion_vit = nn.MSELoss()
    optimizer_vit = torch.optim.Adam(model_vit.parameters(), lr=lr)

    train_dataset = GazeEstimationDataset(image_paths, landmark_data, gaze_coordinates)
    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    model_vit.train()
    for epoch in range(num_epochs):
        for batch_idx, (images, _, gaze_coordinates) in enumerate(train_loader):
            optimizer_vit.zero_grad()
            outputs_vit = model_vit(images)
            loss_vit = criterion_vit(outputs_vit, gaze_coordinates)
            loss_vit.backward()
            optimizer_vit.step()

    torch.save(model_vit.state_dict(), save_path)
