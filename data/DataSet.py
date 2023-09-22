import csv
import os
import pandas as pd
#TODO add monitor size data if needed
class DataSet:
    def __init__(self, csv_file_path, frames_file_name='images_data.csv', landmarks_file_name='landmarks_data.csv', gazes_file_name='gaze_data.csv'):
        self.csv_file_path = csv_file_path
        self.faces_file_name = faces_file_name
        self.landmarks_file_name = landmarks_file_name
        self.gaze_file_name = gaze_file_name
        
    def write_frameData_to_csv(self, index, frame_path, landmarks, gaze):
        #consider that frame_path is the path of the image files!
        self.write_frame_path_to_csv(self, index, frame_path)
        self.write_landmarks_to_csv(self, index, landmarks)
        self.write_gaze_to_csv(self, index, gaze_x, gaze_y)
        #TODO add log in here

            
    def write_frame_path_to_csv(self, index, frame_path):
        full_file_path = os.path.join(self.csv_file_path, self.frames_file_name)

        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Frame_path']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Frame_path']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Index': index, 'Frame_path': frame_path})
            
    def write_landmarks_to_csv(self, index, landmarks):
        full_file_path = os.path.join(self.csv_file_path, self.landmarks_file_name)

        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Category', 'X', 'Y']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Category', 'X', 'Y']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)x

            for category_data in landmarks:
                category_name = category_data['name']
                for x, y in category_data['landmarks']:
                    writer.writerow({'Index': index, 'Category': category_name, 'X': x, 'Y': y})
                    
    def write_gaze_to_csv(self, index, gaze_x, gaze_y):
        full_file_path = os.path.join(self.csv_file_path, self.gaze_file_name)

        if not os.path.exists(full_file_path):
            with open(full_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['Index', 'Gaze_X', 'Gaze_Y']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(full_file_path, mode='a', newline='') as csv_file:
            fieldnames = ['Index', 'Gaze_X', 'Gaze_Y']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Index': index, 'Gaze_X': gaze_x, 'Gaze_Y': gaze_y})

    def load_by_index(self, index):
        
    def load_landmarks_from_csv(self):
        landmarks_data = {}
        with open(os.path.join(self.csv_file_path, self.landmarks_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                index = int(row['Index'])
                category = row['Category']
                x = int(row['X'])
                y = int(row['Y'])

                if index not in landmarks_data:
                    landmarks_data[index] = {'index': index, 'landmarks': []}

                landmarks_data[index]['landmarks'].append({'category': category, 'x': x, 'y': y})

        index_landmarks_pairs = list(landmarks_data.values())
        return index_landmarks_pairs
    
    def load_gaze_from_csv(self):
        gaze_data = {}
        with open(os.path.join(self.csv_file_path, self.gaze_file_name), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                index = int(row['Index'])
                gaze_x = int(row['Gaze_X'])
                gaze_y = int(row['Gaze_Y'])

                gaze_data[index] = {'index': index, 'gaze_x': gaze_x, 'gaze_y': gaze_y}

        gaze_pairs = list(gaze_data.values())
        return gaze_pairs


    def combine_csv_files(self, output_file_name='combined_data.csv'):
        landmarks_df = pd.read_csv(os.path.join(self.csv_file_path, self.landmarks_file_name))
        gaze_df = pd.read_csv(os.path.join(self.csv_file_path, self.gaze_file_name))

        # Merge the dataframes based on 'Index'
        combined_df = pd.merge(landmarks_df, gaze_df, on='Index')

        # Rename columns to match the specified format
        combined_df.rename(columns={'X': 'Landmark_X', 'Y': 'Landmark_Y', 'Gaze_X': 'Gaze_X', 'Gaze_Y': 'Gaze_Y'}, inplace=True)

        # Reorder columns to match the desired format
        combined_df = combined_df[['Index', 'Category', 'Landmark_X', 'Landmark_Y', 'Gaze_X', 'Gaze_Y']]

        # Save the combined dataframe to a new CSV file
        combined_df.to_csv(os.path.join(self.csv_file_path, output_file_name), index=False)

    def read_combined_csv(self, combined_file_name='combined_data.csv'):
        combined_file_path = os.path.join(self.csv_file_path, combined_file_name)
        combined_df = pd.read_csv(combined_file_path)
        return combined_df

if __name__ == "__main__":
    csv_file_path = '/'  
