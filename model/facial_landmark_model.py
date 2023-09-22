# facial_landmark_model.py
import torch
import torch.nn as nn

class FacialLandmarkModel(nn.Module):
    def __init__(self, num_output_units):
        super(FacialLandmarkModel, self).__init__()

        # Branches for each eye and pupil
        self.branch_right_eye = self.create_branch(landmark_size, 64)  # Adjust input size and hidden units
        self.branch_left_eye = self.create_branch(landmark_size, 64)
        self.branch_pupil_right = self.create_branch(landmark_size, 64)
        self.branch_pupil_left = self.create_branch(landmark_size, 64)
        self.branch_face_grid = self.create_branch(landmark_size, 64)

        # Combine each eye with its respective pupil using weighted combinations
        self.combine_right_eye = self.create_combine_layer(128)  # Combine right_eye and pupil_right
        self.combine_left_eye = self.create_combine_layer(128)  # Combine left_eye and pupil_left

        # Learnable parameters (weights) for combining features
        self.weight_right_eye = nn.Parameter(torch.randn(128))  # Adjust size as needed
        self.weight_left_eye = nn.Parameter(torch.randn(128))  # Adjust size as needed

        # Combine the outputs from both eyes and the face_grid using weighted combinations
        self.final_combine = self.create_combine_layer(384)  # Combine combine_right_eye, combine_left_eye, and branch_face_grid

        # Fully connected layer for final output
        self.fc = nn.Linear(384, num_output_units)  # Adjust input and output units

    def create_branch(self, input_size, hidden_units):
        return nn.Sequential(
            nn.Linear(input_size, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU()
        )

    def create_combine_layer(self, input_size):
        return nn.Sequential(
            nn.Linear(input_size, input_size),
            nn.ReLU()
        )

    def forward(self, right_eye, left_eye, pupil_right, pupil_left, face_grid):
        # Process each eye, pupil, and face_grid branch separately
        out_right_eye = self.branch_right_eye(right_eye)
        out_left_eye = self.branch_left_eye(left_eye)
        out_pupil_right = self.branch_pupil_right(pupil_right)
        out_pupil_left = self.branch_pupil_left(pupil_left)
        out_face_grid = self.branch_face_grid(face_grid)

        # Combine each eye with its respective pupil using weighted combinations
        combined_right_eye = self.combine_right_eye(torch.cat((out_right_eye, out_pupil_right), dim=1))
        combined_left_eye = self.combine_left_eye(torch.cat((out_left_eye, out_pupil_left), dim=1))

        # Apply weights to the combined eye features
        combined_right_eye = combined_right_eye * self.weight_right_eye.unsqueeze(0)  # Broadcasting to match batch size
        combined_left_eye = combined_left_eye * self.weight_left_eye.unsqueeze(0)

        # Combine the outputs from both eyes and the face_grid using weighted combinations
        final_combined = self.final_combine(torch.cat((combined_right_eye, combined_left_eye, out_face_grid), dim=1))

        # Fully connected layer for final output
        output = self.fc(final_combined)

        return output
