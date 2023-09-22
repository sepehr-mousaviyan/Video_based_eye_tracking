# gaze_estimation_model.py
import torch
import torch.nn as nn
from pytorch_pretrained_vit import ViT

class GazeEstimationModel(nn.Module):
    def __init__(self, facial_landmark_model, num_output_units):
        super(GazeEstimationModel, self).__init__()

        # Fine-tuned ViT model for image input
        self.image_model = ViT('B_16_imagenet1k', pretrained=True)

        # Facial landmark model (loaded with pretrained weights)
        self.facial_landmark_model = facial_landmark_model

        # Fusion layer for combining image, ViT, and landmarks data
        self.fusion_layer = nn.Sequential(
            nn.Linear(self.image_model.fc.in_features + self.facial_landmark_model.fc.in_features, 256),
            nn.ReLU(),
            nn.Linear(256, num_output_units)  # Output layer for gaze estimation
        )

    def forward(self, image, landmarks):
        # Forward pass for image data through the fine-tuned ViT model
        image_features = self.image_model(image)

        # Forward pass for landmark data through the facial landmark model
        landmarks_features = self.facial_landmark_model(landmarks)

        # Concatenate image and landmarks features
        combined_features = torch.cat((image_features, landmarks_features), dim=1)

        # Forward pass through the fusion layer for gaze estimation
        gaze_estimates = self.fusion_layer(combined_features)

        return gaze_estimates
