
import segno
import zlib
import math
import cv2
import numpy as np
import os

# Generates multiplex QR code
def generate_qr(data, version=None, error_correction_level=None, multiplexed=False):
    # Clear out folder
    if os.path.exists("out"):
        os.rmdir("out")
    print("Generating QR code...")
    # Converts data 
    data = data.to_bytes()
    # Compresses data
    data = compress_data(data)
    print("Data compressed: " + str(len(data)) + " bytes")
    # Calculates the minimum number of QR codes needed to store the data
    required_qrs = calculate_required_qrs(data)
    print("Required QR codes: " + str(required_qrs))
    if multiplexed:
        # Calculate most efficient number of splits required
        splits = required_qrs + (3-required_qrs%3)
        # Splits data across 3 QR codes, interleaving the data
        splits = split_data(data, splits)
        print(f"Split data across {str(splits//3)} Multiplexed QR codes")
        for i in range(splits//3):
            # Clear the temp folder
            if os.path.exists("temp"):
                os.rmdir("temp")
            # Generates QR code for each color channel
            red_qr = segno.make(splits[i], version=version, error=error_correction_level, micro=False, dark="red", data_dark="red", data_light="white", light="white")
            green_qr = segno.make(splits[i+1], version=version, error=error_correction_level, micro=False, dark="green", data_dark="green", data_light="white", light="white")
            blue_qr = segno.make(splits[i+2], version=version, error=error_correction_level, micro=False, dark="blue", data_dark="blue", data_light="white", light="white")
            # Saves QR codes
            red_qr.save("temp/red_qr.png", scale=10)
            green_qr.save("temp/green_qr.png", scale=10)
            blue_qr.save("temp/blue_qr.png", scale=10)
            # Merges QR codes
            multiplex_qrs("temp/red_qr.png", "temp/green_qr.png", "temp/blue_qr.png", i)
    else:
        # Generates QR codes):
        segno.make_sequence(data, version=version, error=error_correction_level, micro=False, dark="black", data_dark="black", data_light="white", light="white").save("out/qr_code.png", scale=10)
def multiplex_qrs(red_qr, green_qr, blue_qr, i):
    print(f"Multiplexing QR codes [{i}]... ")
    # Load the images
    red = cv2.imread(red_qr)
    green = cv2.imread(green_qr)
    blue = cv2.imread(blue_qr)
    #Convert to numpy arrays
    red = np.array(red)
    green = np.array(green)
    blue = np.array(blue)

    # Convert the images to RGB
    red = cv2.cvtColor(red_qr, cv2.COLOR_RGB2GRAY)
    green = cv2.cvtColor(green_qr, cv2.COLOR_RGB2GRAY)
    blue = cv2.cvtColor(blue_qr, cv2.COLOR_RGB2GRAY)

    multiplexed_qr_code = cv2.merge([red, green, blue])
    
    #Save the multiplexed_qr_code as a png file
    cv2.imwrite(f"out/multiplexed_qr_code_{i}.png", multiplexed_qr_code)
    print(f"Multiplexed QR codes [{i}] saved to out/multiplexed_qr_code_{i}.png")

    return multiplexed_qr_code

    
# Interleave and splits data across splits number of QR codes
def split_data(data, splits):
    # Create splits number of bins for the data to be split into
    bins = [[] for i in range(splits)]
    # Interleave the data
    for i in range(len(data)):
        bins[i % splits].append(data[i])
    # Convert the data into bytes
    bins = [bytes(bin) for bin in bins]
    return bins

# Uses lossless compression to compress data TODO: Maybe we might want to use lossy compression?
def compress_data(data, lossless=True):
    if lossless:
        # Perform lossless compression on the data
        data = zlib.compress(data)
    else:
        # Perform lossy compression on the data
        NotImplemented
    return data

# Calculate the minimum number of QR codes needed to store the data, assume highest version and lowest error correction level
def calculate_required_qrs(data, version=40, error_correction_level="L"):
    return math.ceil(len(data) / segno.max_data_capacity(version, error_correction_level))


