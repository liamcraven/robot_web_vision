import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
import zlib

def read_qr(img, multiplexed=True):
    """
    This function reads the QR code from an image.
    """
    data = None
    if multiplexed:
        # Split the image into the 3 colour channels
        (red_image, green_image, blue_image) = demultiplexer(img)
        # Read the QR code from each channel
        red_data = read_qr_channel(red_image)
        green_data = read_qr_channel(green_image)
        blue_data = read_qr_channel(blue_image)
        # Interleave the data
        data = deinterleaving(red_data, green_data, blue_data)
    else:
        data = read_qr_channel(img)
    #Decompress data
    data = decompress(data)
    return data

def demultiplexer(img):
    """
    This function splits the image into the 3 colour channels.
    """
    # Use the opencv module to split the image into the 3 colour channels
    (red_image, green_image, blue_image) = cv2.split(img)
    return (red_image, green_image, blue_image)

def deinterleaving(data):
    """
    This function deinterleaves the data from the 3 colour channels.
    """
    # Interleave and split the data so that it is spread across all 3 channels of the QR code
    red_data = bytearray()
    green_data = bytearray()
    blue_data = bytearray()

    for i in range(0, len(data), 3):
        red_data += data[i].to_bytes(1, byteorder='big')
        green_data += data[i+1].to_bytes(1, byteorder='big')
        blue_data += data[i+2].to_bytes(1, byteorder='big')
    if len(data) % 3 == 1:
        red_data += data[-1].to_bytes(1, byteorder='big')
    elif len(data) % 3 == 2:
        red_data += data[-2].to_bytes(1, byteorder='big')
        green_data += data[-1].to_bytes(1, byteorder='big')
    return (red_data, green_data, blue_data)

def decompress(data):
    """
    This function decompresses the data.
    """
    # Decompress the data
    decompressed_data = zlib.decompress(data)
    return decompressed_data


def read_qr_channel(img):
    """
    This function reads the QR code from a single channel.
    """
    # Use the pyzbar module to read the QR code
    decoded = pyzbar.decode(img)
    # Extract the data from the QR code
    data = decoded[0].data.decode('utf-8')
    return data
