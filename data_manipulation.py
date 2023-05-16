import torch
import numpy as np

# Encoding Tools
def data_serialization(data_path): #TODO: Implement 
    data = NotImplemented
    return data

def data_compression(data): #TODO: Implement 
    data = NotImplemented
    return data

def prepare_data(data_path): #TODO: Implement 
    """
    This function prepares the data for encoding.
    """
    # Serialise data
    data = torch.load(data_path)
    return data


# Decoding Tools

def data_decompression(data): #TODO: Implement 
    """
    This function decompresses the data.
    """
    # Use the zlib module to decompress the data
    data = NotImplemented
    return data

def data_deserialization(data): #TODO: Implement 
    """
    This function deserializes the data.
    """
    # Use the pickle module to deserialize the data
    data = NotImplemented
    return data

def combine_data(red_data, green_data, blue_data): #TODO: Implement 
    """
    This function combines the data from the 3 colour channels.
    """
    # Use the opencv module to combine the 3 channels into a single image
    data = NotImplemented
    return data

def data_extraction(data): #TODO: Implement 
    """
    This function extracts the data from the data.
    """
    # Use the opencv module to extract the data from the data
    data = NotImplemented
    return data

