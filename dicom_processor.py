import os
import argparse
import pydicom
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import Utility_functions as uf
pydicom.config.settings.reading_validation_mode = pydicom.config.IGNORE

# Reads .dicom files, extracts metadata and preprocesses the images. 
# Saves images as .png and metadata as .csv to specified output directory.
# Merges train.csv dataframe from dataset with metadata from dicom files.

def main(input_path, output_dir, train_path, is_folder, apply_resize, size, keep_ratio, apply_denoise, method):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    metadata_list = []

    if is_folder:
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.dicom')]
    else:
        files = [input_path]
    
    for file in files:
        print(f"Processing: {file}")
        metadata = uf.extract_metadata(file)
        if metadata:
            metadata_list.append(metadata)

        processed_image = uf.process_image(file)
        
        if apply_resize:
            new_image = uf.resize_image(processed_image, size, keep_ratio)
            if apply_denoise:
                new_image = uf.denoise(new_image, method)
        else:
            new_image = processed_image
            if apply_denoise:
                new_image = uf.denoise(new_image, method)
        
        if new_image is not None:
            output_path = os.path.join(output_dir, os.path.basename(file).replace('.dicom', '.png'))
            uf.save_image(new_image, output_path)

    metadata_df = pd.DataFrame(metadata_list)
    train_df = pd.read_csv(train_path)
    metadata_df = pd.merge(metadata_df, train_df, on='image_id', how='left')
    metadata_csv_path = os.path.join(output_dir, "metadata.csv")
    metadata_df.to_csv(metadata_csv_path, index=False)
    print(f"Metadata saved to {metadata_csv_path}")

# Entry Point

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DICOM Image Processor")
    parser.add_argument('input', help="Path to input file or folder")
    parser.add_argument('output', help="Path to output folder")
    parser.add_argument('train_path', help="Path to train set metadata")
    parser.add_argument(
        '-f', '--is_folder', 
        action='store_true', 
        help="Set this flag if input is a folder"
    )
    parser.add_argument(
        '-r', '--apply_resize', 
        action='store_true', 
        help="Set this flag to apply resize function"
    )
    parser.add_argument(
        '-s', '--size', 
        type=int,
        default=256,
        help="Enter desired size, default 256"
    )
    parser.add_argument(
        '-k', '--keep_ratio', 
        action='store_true', 
        help="Set this flag to keep ratio when resizing"
    )
    parser.add_argument(
        '-d', '--apply_denoise',
        action='store_true',
        help='Set this flag to apply denoise technique'
    )
    parser.add_argument(
        '-m', '--method', 
        type=str,
        default='Gaussian',
        help="Enter desired denoising method ('Gaussian', 'Median'), default Gaussian"
    )
    args = parser.parse_args()

    main(args.input, args.output, args.train_path, args.is_folder, args.apply_resize, args.size, args.keep_ratio, args.apply_denoise, args.method)
