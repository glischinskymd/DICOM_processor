import os
import argparse
import pandas as pd
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

# Prints a preprocessed image, in its original size, with all annotated bounding boxes.
# Required input: folder path to image, image path, dataframe path
# Bounding box colors are randomly generated upon use.

label2color = {}
viz_labels = ['Aortic enlargement', 'Atelectasis', 'Calcification', 'Cardiomegaly', 'Consolidation', 'ILD', 'Infiltration', 'Lung Opacity', 
                  'Nodule/Mass', 'Other lesion', 'Pleural effusion', 'Pleural thickening', 'Pneumothorax', 'Pulmonary fibrosis']
for i, label in enumerate(viz_labels):
    label2color[label] = [random.randint(0, 255) for i in range(3)]

def main(image_folder, image_path, df_path):
    thickness = 6

    image = cv2.imread(os.path.join(image_folder, image_path))
    df = pd.read_csv(df_path)

    image_data = df['image_id'] == image_path.rstrip('.png')
    coordinates = ['class_name', 'x_min', 'x_max', 'y_min', 'y_max']
    bbox_data = df.loc[image_data, coordinates]

    for i, row in bbox_data.iterrows():
        if row['class_name'] != 'No finding':
            x_min = int(row['x_min'])
            x_max = int(row['x_max'])
            y_min = int(row['y_min'])
            y_max = int(row['y_max'])
            class_name = row['class_name']
            color = label2color[class_name]
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
            cv2.putText(image, class_name, (x_min, y_min + 60), cv2.FONT_HERSHEY_COMPLEX, 3, color, 6)

        else:
            print(f'No bounding boxes found for image {image_path}')

    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(image)
    ax.axis('off')
    plt.show()
    
# Entry point

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bounding boxes")
    parser.add_argument('image_folder', help='path to image files')
    parser.add_argument('image_path', help='desired image path')
    parser.add_argument('df', help='path to dataframe with annotated bounding boxes')
    args = parser.parse_args()
    main(args.image_folder, args.image_path, args.df)