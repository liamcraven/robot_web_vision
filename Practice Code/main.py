import argparse # Importing the argparse module

# import qrcode as qr # Importing the qrcode module
# from reedsolo import RSCodec, ReedSolomonError # Importing the reedsolo module
# import cv2 # Importing the opencv module
# import torch # Importing the pytorch module
# import numpy as np # Importing the numpy module


from encoding import encoder
from decoding import decoder

"""
We want to generate our own custom QR multiplexed colour qr code which utilises read solomon error correction to prioritise specific data codewords for recovery.
Initial Approach:
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
QR Code Decoding:
    - Image Capture: Define a function to capture an image of the QR code.
    - Color Decoding: Split the QR code back into the 3 individual colour channels
    - QR Code Decoding: Use the qrcode module to decode the QR code for each of the colour channels
    - Error Correction: Use the reedsolo module to correct the errors in the data
    - Data Extraction: Extract the data from the QR code
    - Data Decompression: If the data was compressed, decompress the data
    - Data Deserialization: Deserialize the data back into tensors

Main Function: Define a main function to control the flow of the program, this should allow the user to select
the mode of operation (encode or decode), the data to encode or decode, the error correction level, and
the version of the QR code to use.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Define the mode of operation (encode or decode), the data to encode or decode, the error correction level, and the version of the QR code to use.")
    #Chooses the mode of operation
    parser.add_argument("-m","--mode", help="The mode of operation (encode or decode)", choices=["encode", "decode"], required=True)
    #Information for encoder
    parser.add_argument("-d", "--data", help="The data to encode or decode", default="Example Messages\example_messages.pt")
    parser.add_argument("-ecl","--error_correction_level", help="The error correction level to use (L, M, Q, H)", choices=["L", "M", "Q", "H"], default="L")
    parser.add_argument("-v", "--version", help="The version of the QR code to use", choices=range(1, 41), default=1)
    parser.add_argument("-eo","--encoder_save_path", help="The path to save the QR code to", default="qr_code.png")
    #Information for decoder
    parser.add_argument("-in","--load_path", help="The path to load the QR code from", default="qr_code.png")
    parser.add_argument("-do", "--decoder_save_path", help="The path to save the decoded data to", default="decoded_data.txt")
    args = parser.parse_args()
    if args.mode == "encode":
        encoder(args.data, args.error_correction_level, args.version, args.encoder_save_path)
    elif args.mode == "decode":
        decoder(args.load_path, args.decoder_save_path)
