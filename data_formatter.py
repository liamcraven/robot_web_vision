import numpy as np
from binary_data import BinaryData
import reedsolo
import json



class DataFormatter:
    
    
    def __init__(self, file_name):
        
        # Stores the number of error correction codewords per part
        self.EC_CODEWORDS_PER_PART = {
            "int": 10,
            "msb": 5,
            "lsb": 2,
        }
        
        # Stores the original data
        data_arrays = []
        with open(file_name, "r") as f:
            # Load the data from the json file
            data_dict = json.load(f)
        
        # Extract the data from the dictionary
        data_arrays.append(np.array(data_dict["linearization_points"]).reshape(1,3, 2))
        data_arrays.append(np.array(data_dict["factor_to_variable_messages"]["message means"]))
        data_arrays.append(np.array(data_dict["factor_to_variable_messages"]["message precisions"]))
        data_arrays.append(np.array(data_dict["variable_to_factor_messages"]["message means"]))
        data_arrays.append(np.array(data_dict["variable_to_factor_messages"]["message precisions"]))
        
        self.lin_points_shape = data_arrays[0].shape
        self.f2v_shape = data_arrays[1].shape
        self.v2f_shape = data_arrays[3].shape
        
        self.original_data = np.array([])
        for array in data_arrays:
            flat = array.flatten()
            self.original_data = np.concatenate((self.original_data, flat))
            
        #print(self.original_data)

        # Split the data into 3 parts and pass each part to BinaryData in byte format
        self.data_int, self.data_msb, self.data_lsb = self.split_data(self.original_data)
        #print(self.data_int)
        #print(self.data_msb)
        #print(self.data_lsb)
        #print(self.combine_floats()) #TODO: Remove later
        self.data_int = BinaryData(self.data_int.astype(np.int16).tobytes())
        self.data_msb = BinaryData(self.data_msb.astype(np.int32).tobytes())
        self.data_lsb = BinaryData(self.data_lsb.astype(np.int32).tobytes())
        
        # Stores ec codewords
        self.ecdata_int = None
        self.ecdata_msb = None
        self.ecdata_lsb = None
            
    def split_float(self, f, precision=6): #TODO: May need to adapt this
        """
        This function splits float into 3 sections: integer part, most significant decimal part, least significant decimal part.
        The total number of bits used over the 3 parts should not exceed 64 bits and we should preserve the sign of the float.
        """
        #Split float into integer and fractional parts
        i, frac = divmod(f, 1)

        #Convert the fractional part to a string with a given precision
        frac_str = "{:.{}f}".format(frac, precision)
        
        #Split the fractional part into the most significant and least significant halves
        msb = int(frac_str[2:(precision//2)+2])
        lsb = int(frac_str[(precision//2)+2:])

        return (i, msb, lsb)

    
    def combine_floats(self, precision=6):
        array = []
        
        for i in range(len(self.data_int)):
            divisor = 10 ** (precision//2)
            frac = self.data_msb[i] / divisor + self.data_lsb[i] / (10 ** precision)
            f = self.data_int[i] + frac
            array.append(f)
           
        return array
    
    def split_data(self, data):
        """
        This function splits an array of floats into 3 sections: integer part, most significant decimal part, least significant decimal part.
        The array shape is preserved
        """
        #Split the array into its 3 parts
        int_part, msb, lsb = np.vectorize(self.split_float, otypes=[np.int16, np.int32, np.int32])(data) #May need to change

        return int_part, msb, lsb
    
    def compress(self):
        """
        This function compresses the data.
        """
        self.data_int.compress_data()
        self.data_msb.compress_data()
        self.data_lsb.compress_data()
        
    def total_codewords(self):
        """
        This function returns the number of codewords required to store the data.
        """
        return len(self.data_int.as_codewords()) + len(self.data_msb.as_codewords()) + len(self.data_lsb.as_codewords())
    
    def determine_qr_version(self):
        """
        This function determines the QR version required to store the data.
        """
        
        

    def generate_error_correction(self):
        """
        This function generates and appends error correction codewords to the data.
        It does so by prioritising the data in the following order:
        1. Integer part
        2. Most significant decimal part
        3. Least significant decimal part
        And therefore we allocate more ec codewords to the higher priority data.

        This is called "concatenated coding". #TODO: Remove this comment
        """
        # Calculate the total number of codewords needed for the data
        total_codewords = self.total_codewords()
        
        # Calculate the number of error correction to allocate for each part
        # Normally we have: ec_codewords = data_bytes * total_ec_codewords / qr capacity
        ec_codewords_int = self.EC_CODEWORDS_PER_PART["int"] * len(self.data_int.as_codewords()) // total_codewords
        ec_codewords_msb = self.EC_CODEWORDS_PER_PART["msb"] * len(self.data_msb.as_codewords()) // total_codewords
        ec_codewords_lsb = self.EC_CODEWORDS_PER_PART["lsb"] * len(self.data_lsb.as_codewords()) // total_codewords
        print(ec_codewords_int)
        print(ec_codewords_msb)
        print(ec_codewords_lsb)
        
        # Generate the error correction codewords for each data part
        self.ecdata_int = reedsolo.RSCodec(ec_codewords_int).encode([int.from_bytes(b, 'big') for b in self.data_int.as_codewords()])
        self.ecdata_msb = reedsolo.RSCodec(ec_codewords_msb).encode([int.from_bytes(b, 'big') for b in self.data_msb.as_codewords()])
        self.ecdata_lsb = reedsolo.RSCodec(ec_codewords_lsb).encode([int.from_bytes(b, 'big') for b in self.data_lsb.as_codewords()])
        
        print(len(self.data_int.as_codewords()))
        print(len(self.data_msb.as_codewords()))
        print(len(self.data_lsb.as_codewords()))
        print(len(self.ecdata_int))
        print(len(self.ecdata_msb))
        print(len(self.ecdata_lsb))

        

        
        
        
        
        

        
    
    

    
        