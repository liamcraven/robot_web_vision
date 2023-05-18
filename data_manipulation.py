import torch
import numpy as np

def np_to_binary(data):
    """
    This function converts the dictionary of numpy arrays to a single bytestring.
    """
    bin_data = data["linearization_point"].tobytes()
    bin_data += data["factor_to_variable_messages"]["message mean"].tobytes()
    bin_data += data["factor_to_variable_messages"]["message precision"].tobytes()
    bin_data += data["variable_to_factor_messages"]["message mean"].tobytes()
    bin_data += data["variable_to_factor_messages"]["message precision"].tobytes()

    return bin_data

# Encoding Tools
def data_serialization(data_path): #TODO: Implement 
    data = NotImplemented
    return data

def data_compression(data): #TODO: Implement 
    data = NotImplemented
    return data

def prepare_data(data_path): #TODO: Test
    """
    This function prepares the data for encoding.
    """
    # Serialise data
    data = torch.load(data_path)

    lin_point = data["linearization point"].numpy()
    f2v = data["factor to variable messages"]
    v2f = data["variable to factor messages"]

    f2v_msg_mean = f2v["message mean"].numpy()
    f2v_msg_precision = f2v["message precision"].numpy()

    v2f_msg_mean = v2f["message mean"]
    v2f_msg_precision = v2f["message precision"].numpy()

    #Convert to numpy array from torch tensor

    """
    lin_point = lin_point.numpy()

    f2v_msg_mean = f2v_msg_mean.numpy()
    f2v_msg_precision = f2v_msg_precision.numpy()

    v2f_msg_mean = v2f_msg_mean.numpy()
    v2f_msg_precision = v2f_msg_precision.numpy()

    """

    # Convert the data back to a dictionary
    data = {"linearization_point": lin_point, "factor_to_variable_messages": {"message mean": f2v_msg_mean, "message precision": f2v_msg_precision}, "variable_to_factor_messages": {"message mean": v2f_msg_mean, "message precision": v2f_msg_precision}}
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

