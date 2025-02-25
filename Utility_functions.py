import pydicom
import numpy as np
import cv2
from PIL import Image
pydicom.config.settings.reading_validation_mode = pydicom.config.IGNORE

# Utility Functions

def extract_metadata(file_path):
# Input: path to files. Extracts metadata from .dicom files, returning a dataframe.
    try:
        dicom_file = pydicom.dcmread(file_path)
        metadata = {
            "image_id": dicom_file.file_meta.MediaStorageSOPInstanceUID,
            "Age": int(dicom_file.PatientAge[1:3]) if 'PatientAge' in dicom_file 
            and (len(dicom_file.PatientAge) == 4)
            and dicom_file.PatientAge != '000Y' 
            else 'NaN',
            "Sex": dicom_file.PatientSex if 'PatientSex' in dicom_file 
            and (dicom_file.PatientSex == 'M' or dicom_file.PatientSex == 'F') 
            else 'NaN',
            "Class_UID": dicom_file.file_meta.MediaStorageSOPClassUID,
        }
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def process_image(file_path, apply_voi=True, fix_monochrome=True):
# Input: path to files. Extracts pixel array, applies VOI LUT, standardises photometric interpretation, normalises pixel values.
    try:
        dicom_file = pydicom.dcmread(file_path)
        image_array = dicom_file.pixel_array

        if apply_voi:
            image_array = pydicom.pixels.apply_voi_lut(image_array, dicom_file)

        if fix_monochrome and dicom_file.PhotometricInterpretation == 'MONOCHROME1':
            image_array = np.amax(image_array) - image_array

        image_array = (image_array - np.min(image_array)) / (np.max(image_array) - np.min(image_array))
        image_array = (image_array * 255).astype(np.uint8)

        return image_array
    except Exception as e:
        print(f"Error processing image: {e}")
        return None
    
def resize_image(image_array, size, keep_ratio=False):
# Input: np pixel array. Resizes image to desired size. Default size 256. Optional: keep image ratio, default=False.
    pil_image = Image.fromarray(image_array)
    if keep_ratio:
        pil_image.thumbnail((size, size))
        resized_image = np.array(pil_image)
        return resized_image
    else:
        resized_image = np.array(pil_image.resize((size, size)))
        return resized_image
    
def denoise(array, method, ksize, sigmaX):
# Input: path to .png image. Applies denoising technique. Default='Gaussian', optional, 'Median'
    if method == 'Gaussian':
        denoised_image =cv2.GaussianBlur(array, (ksize, ksize), sigmaX)
    elif method == 'Median':
        denoised_image =(cv2.medianBlur(array, ksize))
    return denoised_image

def save_image(image_array, output_path):
# Input: np pixel array and output folder path. Saves processed image as .png
    try:
        cv2.imwrite(output_path, image_array)
        print(f"Saved image to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")