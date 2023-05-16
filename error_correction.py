from reedsolo import RSCodec, ReedSolomonError # Importing the reedsolo module
import torch # Importing the pytorch module
import numpy as np # Importing the numpy module
import struct # Importing the struct module

# TODO: Why do we bother returning the lsb? Surely this is wasted? We have removed this for now, maybe add back in later if we need it.
def ec_codeword_generation(array): #TODO: Test
    """
    This function calculates and acquires the codewords we would like to target with error correction.
    """
    #In order to do this we want to flatten the numpy array, apply error correction to the most significant bits of each float, and then reshape the array back to its original shape.
    rs = RSCodec(2) # 2 is the number of error correction bytes we want to use
    shape = array.shape #Stores original shape of array
    floats = array.flatten()
    combined = np.array([])
    for float in floats:
        float = float.view(np.float64) #Convert to 64 bit float
        #We want to convert the float to a byte array
        bytearray = struct.pack('f', float) 
        #Split the byte array into most significant bits and least significant bits
        msb = bytearray[0:2] # most significant bits (2 bytes)
        lsb = bytearray[2:8] # least significant bits (6 bytes)
        #Apply error correction to the most significant bits
        msb = rs.encode(msb)
        #Convert the byte array back to a float
        float = struct.unpack('f', bytearray)
        #Convert the float back to a numpy float
        combined = np.append(combined, np.array(float).astype(np.float32))
    #Reshape the array back to its original shape
    array = combined.reshape(shape)
    return array

def error_correction_encoding(data, error_correction_level, version): #TODO: Test
    """
    This function adds error correction to the data.
    """
    # We want to traverse the dictionary and apply error correction to the most significant bits of each individual float in the np array
    #In order to do this we want to flatten the numpy array, apply error correction to the most significant bits of each float, and then reshape the array back to its original shape.
    # Lets begin with linearization point
    ec_data = {}

    # We use the ec_codeword_generation function to generate the error correction codewords
    lp_shape = data["linearization_point"].shape
    ec_data["linearization_point"] = ec_codeword_generation(data["linearization_point"])

    # Now lets do the factor to variable messages
    f2v_mm_shape_ = data["factor_to_variable_messages"]["message mean"].shape
    ec_data["factor_to_variable_messages"] = {}
    ec_data["factor_to_variable_messages"]["message mean"] = ec_codeword_generation(data["factor_to_variable_messages"]["message mean"])
    f2v_mp_shape = data["factor_to_variable_messages"]["message precision"].shape
    ec_data["factor_to_variable_messages"]["message precision"] = ec_codeword_generation(data["factor_to_variable_messages"]["message precision"])

    # Now lets do the variable to factor messages
    v2f_mm_shape = data["variable_to_factor_messages"]["message mean"].shape
    ec_data["variable_to_factor_messages"] = {}
    ec_data["variable_to_factor_messages"]["message mean"] = ec_codeword_generation(data["variable_to_factor_messages"]["message mean"])
    v2f_mp_shape = data["variable_to_factor_messages"]["message precision"].shape
    ec_data["variable_to_factor_messages"]["message precision"] = ec_codeword_generation(data["variable_to_factor_messages"]["message precision"])

    # We now have the error correction data, we should return it
    return ec_data

def error_correction_decoding(data): #TODO: Implement
    """
    This function decodes the error correction from the data.
    """
    # Use the reedsolo module to decode the error correction from the data
    data = NotImplemented
    return data