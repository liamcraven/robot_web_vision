def color_encoding(data): #TODO: Implement
    """
    This function encodes the data into the 3 colour channels.
    """
    # Interleave and split the data so that it is spread across all 3 channels of the QR code
    (red_data, green_data, blue_data) = interleaving(data)
    # Could include converting data into binary format, then mapping the binary data to colours.
    (red_data, green_data, blue_data) = binary_encoding(red_data, green_data, blue_data)
    return (red_data, green_data, blue_data)

def interleaving(data): #TODO: Implement
    """
    Interleaves data accross all 3 channels of the QR code
    """
    (red_data, green_data, blue_data) = NotImplemented
    return (red_data, green_data, blue_data)

def binary_encoding(red_data, green_data, blue_data): #TODO: Implement - may not be needed
    NotImplemented
    return (red_data, green_data, blue_data)

def multiplexer(red_qr_code, green_qr_code, blue_qr_code): # TODO: Implement
    """
    This function multiplexes the 3 colour channels into a single image.
    """
    # Use the opencv module to combine the 3 channels into a single image
    multiplexed_qr_code = NotImplemented
    return multiplexed_qr_code

# Decoding Tools
def demultiplexer(image): #TODO: Implement
    """
    This function decodes the data from the 3 colour channels.
    """
    # Use the opencv module to split the image into the 3 colour channels
    (red_image, green_image, blue_image) = NotImplemented
    return (red_image, green_image, blue_image)