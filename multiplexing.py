import cv2
import numpy as np

def color_encoding(data): #TODO: Test
    """
    This function encodes the data into the 3 colour channels.
    """
    # Interleave and split the data so that it is spread across all 3 channels of the QR code
    (red_data, green_data, blue_data) = interleaving(data)
    return (red_data, green_data, blue_data)

def interleaving(data): #TODO: Test
    """
    Interleaves data accross all 3 channels of the QR code
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



def multiplexer(red_qr, green_qr, blue_qr): # TODO: Implement
    """
    This function multiplexes the 3 colour channels into a single image.
    """
    # Use the opencv module to combine the 3 channels into a single image

    #We want to convert red_qr to numpy array
    red_qr = np.array(red_qr)
    green_qr = np.array(green_qr)
    blue_qr = np.array(blue_qr)

    red_qr = cv2.cvtColor(red_qr, cv2.COLOR_RGB2GRAY)
    green_qr = cv2.cvtColor(green_qr, cv2.COLOR_RGB2GRAY)
    blue_qr = cv2.cvtColor(blue_qr, cv2.COLOR_RGB2GRAY)

    multiplexed_qr_code = cv2.merge([red_qr, green_qr, blue_qr])
    
    #Save the multiplexed_qr_code as a png file
    cv2.imwrite("multiplexed_qr_code.png", multiplexed_qr_code)

    return multiplexed_qr_code

# Decoding Tools
def demultiplexer(image): #TODO: Implement
    """
    This function decodes the data from the 3 colour channels.
    """
    # Use the opencv module to split the image into the 3 colour channels
    (red_image, green_image, blue_image) = cv2.split(image)

    return (red_image, green_image, blue_image)