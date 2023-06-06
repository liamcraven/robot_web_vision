import json
import numpy as np
import brotli
import math
import reedsolo

class ErrorCorrectionLevel: 
    ordinal: int # 0-3
    format_bits: int # 2 bits

    def __init__(self, ordinal: int, format_bits: int):
        self.ordinal = ordinal
        self.format_bits = format_bits

    LOW = (0, 0b01) # 7% of codewords can be restored
    MEDIUM = (1, 0b00) # 15% of codewords can be restored
    QUARTILE = (2, 0b11) # 25% of codewords can be restored
    HIGH = (3, 0b10) # 30% of codewords can be restored
    
class SignificantLevel:
    string: str
    ordinal: int #This will relate to the number of error correction codewords we generate
    ratio: float #This will be the ratio of error correction codewords to data codewords
    
    def __init__(self, ordinal, string, ratio):
        self.string = string
        self.ordinal = ordinal
        self.ratio = ratio
        
    # TODO: Change ordinal values to reflect the number of error correction codewords we generate
    LOW = (0, "L", 0.1) 
    MEDIUM = (1, "M", 0.3)
    HIGH = (2, "H", 0.6)
        
class BitStream():
    
    def __init__(self):
        self.bit_data = []
    
    def append_bits(self,i, data, num_bits):
        """
            This function appends the specified number of bits to the bitstream
        """
        if self.byte_data[i] == None:
            self.byte_data[i] = []
        for i in range(num_bits-1, -1, -1):
            self.byte_data[i].append((data >> i) & 1)
        
        
    def as_bytes_indexed(self, i) -> bytes:
        byte_data = bytearray()
        byte = 0
        bit_count = 0
        for bit in self.bit_data[i]:
            byte = (byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                byte_data.append(byte)
                byte = 0
                bit_count = 0
        if bit_count > 0:
            byte = byte << (8 - bit_count)
            byte_data.append(byte)
        return bytes(byte_data)
        
        
    
    def as_bytes_all(self) -> bytes:
        byte_data = bytearray()
        byte = 0
        bit_count = 0
        for i in self.byte_data:
            for bit in self.bit_data[i]:
                byte = (byte << 1) | bit
                bit_count += 1
                if bit_count == 8:
                    byte_data.append(byte)
                    byte = 0
                    bit_count = 0
        if bit_count > 0:
            byte = byte << (8 - bit_count)
            byte_data.append(byte)
        return bytes(byte_data)
            
    
    def bit_length(self) -> int:
        length = 0
        for i in self.bit_data:
            length += self.bit_length_indexed(i)
        return length
    
    def bit_length_indexed(self, i) -> int:
        return len(self.bit_data[i])
    
    def get_bit(self, i: int, j: int) -> bool:
        """
            This function returns true if the bit at the specified index is 1, false otherwise
        """
        return self.bit_data[i][j]
            
    def combine_data(self):
        """
            This function combines all the data into a single bitstream along with the mode indicator and character count indicator
        """
        data = BitStream()
        data.append_bits(0, 0b0100, 4) # Mode 
        bit_length = self.bit_length()
        data.append_bits(0, bit_length, 8) # Character count indicator
        data.append_bits(0, self.as_bytes_all(), bit_length) # Data
        return data
            
        
        
            
            
        
            

class QRCodeGen:
    """
        Custom QR Generation class:
        - Input data: JSON dictionary of arrays
        - Data is serialized
        - TODO: Finish this
        - Output: QR code
    """
    
    _ec_codewords_per_block = [
        # Version
        #X, 1,  2,  3, ....
        [0, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],  # Low
		[0,10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],  # Medium
		[0, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],  # Quartile
		[0, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]  # High
    ]
    
    _ec_codeblocks_count = [
        # Number of ec codeblocks
        #X, 1, 2, 3, 4, 5 ....
		[0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4,  4,  4,  4,  4,  6,  6,  6,  6,  7,  8,  8,  9,  9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],  # Low
		[0, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5,  5,  8,  9,  9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],  # Medium
		[0, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8,  8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],  # Quartile
		[0, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81]  # High
    ]
    
    def __init__(self, data_path, ecl: ErrorCorrectionLevel):
        
        with open(data_path, 'r') as f:
            data = json.load(f)
            
        # We first serialize the data whilst keeping track of the shapes
        self.data, self.shapes = self.serialize_data(data)
        
        # We then split the data into integer, most significant decimal and least significant decimal parts
        self.integer_data, self.msd_data, self.lsd_data = self.split_float(self.data)
        
        #Compress the data individually
        self.integer_data = brotli.compress(self.integer_data)
        self.msd_data = brotli.compress(self.msd_data)
        self.lsd_data = brotli.compress(self.lsd_data)
        
        # We then convert the data into bytes
        self.data = self.convert_to_bytes([(SignificantLevel.HIGH,self.integer_data), (SignificantLevel.MEDIUM, self.msd_data), (SignificantLevel.LOW,self.lsd_data)])
        self.version = self.get_min_version(self.data, ecl)
        self.size = self.version * 4 + 17
        self.ecl = ecl #TODO: Boost the ECL if possible
        
        # Generate the EC data for each significance level
        self.integer_ec = self.generate_ec(self.integer_data, self.version, self.ecl, SignificantLevel.HIGH)
        self.msd_ec = self.generate_ec(self.msd_data, self.version, self.ecl, SignificantLevel.MEDIUM)
        self.lsd_ec = self.generate_ec(self.lsd_data, self.version, self.ecl, SignificantLevel.LOW)
        
        # Concatenate the data to create the final bit string
        self.data = self.data.combine_data()

        # Add terminator and convert to bytes
        data_capacity = self.get_version_data_capacity(self.version, self.ecl)
        self.data.append_bits(0, 0,data_capacity - self.data.bit_length())
        self.data = self.data.as_bytes_all()
        
        # Pad with alternating bytes until we reach the data capacity for the version
        # Pad Bytes: 0xEC 0x11
        while(len(self.data) < data_capacity):
            self.data += bytes([0XEC])
            if len(self.data) < data_capacity:
                self.data += bytes([0X11])
                
    def generate_ec(self, data, version, ecl, siglvl: SignificantLevel):
        """
            This function generates the EC data for each significance level, with the number
            of codeblocks proportional to each significance level
        """
        # Get the number of codeblocks for the given significance level
        num_codewords = self.get_ec_codeblocks_count(version, ecl)
        num_codewords = math.floor(num_codewords * siglvl.ratio)
        
        # Generate the EC data for the given significance level
        rs = reedsolo.RSCodec(num_codewords)
        ec_data = rs.encode(data)
        
        return ec_data
        
    
        
        
        
        
        
        
    def get_ec_codeblocks_count(self, version, ecl):
        """
            This function returns the number of EC codeblocks for a given version and ecl
        """
        return self._ec_codeblocks_count[ecl.value][version]
        
    def serialize_data(self, data: dict):
        """
            This function serializes the data into a byte array
        """
        serialized_data = []
        shapes = []
        for key, value in data.items():
            if isinstance(value, dict):
                sub_data, sub_shapes = self.serialize_data(value)
                serialized_data.append(sub_data)
                shapes.append(sub_shapes)
            elif isinstance(value, np.ndarray):
                serialized_data.append(value.flatten().tolist())
                shapes.append(value.shape)
            else: # This should not be reached
                serialized_data.append(value)
        return serialized_data, shapes
    
    def convert_to_bytes(self, data):
        """
            This function converts the array of ints into an array of bytes
        """
        bs = BitStream()
        for (siglvl, d) in data:
            for i in d:
                bs.append_bits(siglvl, i)
        return bs
    
    """
        These functions are resonsible for float splitting in data preparation
    """
    
    
    def split_floats(self, floats):
        """
            Splits array of floats into arrays of their integer and decimal parts
        """
        for float in floats:
            yield self.split_float(float)
            
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
        
    
    def get_min_version(self, data: BitStream, ecl: ErrorCorrectionLevel):
        """
            This function returns the minimum version required to encode the data
        """
        for version in range(1, 41):
            if data.bit_length <= self.get_version_data_capacity(version, ecl):
                return version
        raise ValueError("Data is too large to be encoded in a QR code")
            
    def get_version_data_capacity(self, version: int, ecl: ErrorCorrectionLevel):
        return self.get_raw_module_capacity(version) - self.get_num_ec_modules(version, ecl)
    
    def get_num_ec_modules(self, version: int, ecl: ErrorCorrectionLevel):
        return self._ec_codewords_per_block[ecl.ordinal][version] * self._ec_codeblocks_count[ecl.ordinal][version]
    
    def get_raw_module_capacity(self, version: int):
        num_modules = (16 * version + 128) * version + 64
        if version >= 2:
            num_modules -= (25 * (version // 7 + 2) - 10) * (version // 7 + 2) - 55
            if version >= 7:
                num_modules -= 36
        return num_modules
    
    

class DataPartition:
    
    def __init__(self, data, char_count):
        self.mode_bits = 0x4
        self.char_count = char_count
        self.data = data
        
    def get_mode_bits(self):
        return self.mode_bits
    
    def get_char_count(self):
        return self.char_count
    
    def get_data(self):
        return self.data
        
        
    
        
        
        
        
    
    
    
    

        
        
        
        
        
        
    
