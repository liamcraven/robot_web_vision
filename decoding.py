from data_manipulation import combine_data, data_extraction, data_decompression, data_deserialization
from error_correction import error_correction_decoding
from multiplexing import demultiplexer

import qrcode
import cv2

"""
Decoder Steps:
QR Code Decoding:
    - Image Capture: Define a function to capture an image of the QR code.
    - Color Decoding: Split the QR code back into the 3 individual colour channels
    - QR Code Decoding: Use the qrcode module to decode the QR code for each of the colour channels
    - Error Correction: Use the reedsolo module to correct the errors in the data
    - Data Extraction: Extract the data from the QR code
    - Data Decompression: If the data was compressed, decompress the data
    - Data Deserialization: Deserialize the data back into tensors
"""

def image_capture(load_path): #TODO: Implement - May not need to be a function
    """
    This function captures an image.
    """
    # Use the opencv module to capture an image
    multiplexed_qr = cv2.imread(load_path)
    return multiplexed_qr

def qr_code_decoding(load_path): #TODO: Implement 
    """
    This function decodes the data from the QR code.
    """
    # Get image
    image = image_capture(load_path)

    # Demultiplex the image
    (red_image, green_image, blue_image) = demultiplexer(image)

    # Use the qrcode module to decode the QR code for each of the colour channels
    (red_data, green_data, blue_data) = (scan_qr(red_image), scan_qr(green_image), scan_qr(blue_image))
    return (red_data, green_data, blue_data)


def scan_qr(image):
    # Create a QR code scanner
    qr_scanner = qrcode.QRCode()
    # Add the image to the QR code scanner
    qr_scanner.add_data(image)
    # Decode the QR code
    qr_scanner.decode()
    # Get the data from the QR code
    data = qr_scanner.data
    return data

def save_data(data, decoder_save_path): #TODO: Implement 
    """
    This function saves the data.
    """
    # Save the data as a file
    NotImplemented
    pass

def decoder(load_path, decoder_save_path): #TODO: Implement
    """
    This function decodes the data from a QR code.
    """
    # Image capture - to be changed to a live video feed
    image = image_capture(load_path)
    # Color decoding
    (red_image, green_image, blue_image) = demultiplexer(image)
    # QR code decoding
    (red_data, green_data, blue_data) = qr_code_decoding(red_image, green_image, blue_image)
    # Combine data
    data = combine_data(red_data, green_data, blue_data)
    # Error correction decoding and validation
    data = error_correction_decoding(data)
    # Data extraction
    data = data_extraction(data)
    # Data decompression
    data = data_decompression(data)
    # Data deserialization
    data = data_deserialization(data)
    # Save data
    save_data(data, decoder_save_path)
    pass