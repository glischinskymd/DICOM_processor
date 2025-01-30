dicom_processor:

Main function. Run on terminal.
Input:
- path to file or folder
- output path
- train.csv path
- '-f', '--is_folder'. Tag to identify input as a folder.
- '-r', '--apply_resize'. Tag apply resize. If False, saves images in original size
- '-s'. '--size'. Desired size in int. Default=256
- '-k', '--keep_ratio'. Tag to maintain image ratio. Default=False.


Utility_functions:

extract_metadata(input_folder):
Parameters: 
- input_folder: path to DICOM files
Returns: DataFrame with extracted metadata (Age, Sex, Class_UID, valid UID) from DICOM files.

read_xrays(image_path, VOI_LUT=False, Fix_MONOCHROME=True):
Parameters:
- Image_path: list of DICOM file paths to be read.
- VOI_LUT: bool, default=True. Applies VOI_LUT to DICOM files according to VOI_LUT Module
- Fix_MONOCHROME: bool, default=True. If the file’s Photometric Interpretation tag is MONOCHROME1, convert it to MONOCHROME2.
Returns: List of resized uint8 pixel arrays.

resize(array, size, keep_ratio=False):
Parameters
- List of image pixel arrays.
- Size: int, specified size to resize the images.
- keep_ratio: bool, default=False. If true, maintains image ratios.
Returns a new list of arrays with images resized to the specified size.

denoise(array, Method='Gaussian'):
Parameters
- List of image arrays
- Method: string, default=”Gaussian”. Options: “Gaussian”, “Median”.
Returns a new list of arrays after applying denoising technique.

save_image(pixel_arrays, output_folder): converts and saves pixel arrays to .png
Parameters:
- pixel_arrays: list of preprocessed images
- output_folder: folder path to save images as .png
