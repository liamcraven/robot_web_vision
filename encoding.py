import qrcode

from data_manipulation import prepare_data, np_to_binary
from error_correction import error_correction_encoding
from multiplexing import multiplexer, color_encoding
"""
Encoder Steps: 
Data Preparation:
    - Serialise data: Serialize tensors representing the linearization point,
    factor to variable messages and variable to factor messages. (Pytorch)
Error Correction:
    - Calculate and acquire the codewords that we would like to target with error correction
    - Use the reedsolo module to generate the error correction codewords and add it to our data
Data Compression: Compress Data: If data is too large to fit in a single QR code, we need to
    compress the data. (gzip or zlib) #TODO: Research compression algorithms
Color Encoding:
    - Interleave and split the data so that it is spread across all 3 channels of the QR code
    - Could include converting data into binary format, then mapping the binary data to colours.
QR Code Generation:
    - Use the qrcode module to generate the QR code for each of the colour channels
    - Use the opencv module to combine the 3 channels into a single image
    - Save the image as a png file
"""

def qr_code_generation(red_data, green_data, blue_data, version, ec_level): #TODO: Test
    """
    This function generates the QR code for each of the colour channels.
    """
    # Use the qrcode module to generate the QR code for each of the colour channels
    red_qr_code = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
    red_qr_code.add_data(red_data)
    red_qr_code.make(fit=True)
    red_qr_code = red_qr_code.make_image(fill_color="red", back_color="white")

    green_qr_code = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
    green_qr_code.add_data(green_data)
    green_qr_code.make(fit=True)
    green_qr_code = green_qr_code.make_image(fill_color="green", back_color="white")

    blue_qr_code = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
    blue_qr_code.add_data(blue_data)
    blue_qr_code.make(fit=True)
    blue_qr_code = blue_qr_code.make_image(fill_color="blue", back_color="white")

    return (red_qr_code, green_qr_code, blue_qr_code)


def save_qr_code(multiplexed_qr_code, encoder_save_path): #TODO: Implement 
    """
    This function saves the QR code as a png file.
    """
    # Save the image as a png file
    NotImplemented
    pass

def encoder(data_path, error_correction_level, version, encoder_save_path): #TODO: Implement 
    """
    This function encodes the data into a QR code.
    """
    # Prepare data - we want to get the data into a format that we can use
    data = prepare_data(data_path)
    # Error correction
    ec_data = error_correction_encoding(data, error_correction_level, version)

    # Convert data to binary and combine with EC data
    data = np_to_binary(data)
    ec_data = np_to_binary(ec_data)
    data += ec_data

    # Color encoding
    (red_data, green_data, blue_data) = color_encoding(data)
    # QR code generation
    (red_qr_code, green_qr_code, blue_qr_code) = qr_code_generation(red_data, green_data, blue_data, version, error_correction_level)
    # Multiplexing
    multiplexed_qr_code = multiplexer(red_qr_code, green_qr_code, blue_qr_code)
    # Save QR code
    save_qr_code(multiplexed_qr_code, encoder_save_path)
    pass