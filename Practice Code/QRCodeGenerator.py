"""
I want you to act as my personal programming assistant. With every prompt you will conduct research into the most up to date techniques for solving the given problem, based on research papers and articles. You then must apply such research to the current problem at hand. For context, I am trying to build an application in python that has the following capabilities:

- Be able to transform numpy arrays of 64 bit floats into multiplexed colour QR codes in the most efficient manor possible, prioritising low data capacities and processing speed.
- Have a customized error correction method that gives the QR code the property of representing less precise floats if data is lost. 
- Be able to decode such QR codes to retrieve the original data"""

from reedsolo import RSCodec
import struct
import numpy as np

class MultiplexedQRCodeGenerator:

    def __init__(self, data = None) -> None:
        self.COLOURS = ["red", "green", "blue"]
        self.data = [data] # List of numpy arrays
        self.data_shape = [data.shape]
        self.ec_high_prec = None
        self.ec_med_prec = None
        self.ec_low_prec = None
    
    def add_data(self, data):
        self.data.append(data)
        self.data_shape.append(data.shape)
    
    def generate_qr_code(self, data, save_path):
        # Adds data
        self.add_data(data)
        # Generate QR code
        qr_code = self.make()
        # Save QR code
        qr_code.save(save_path)

        
    def make(self):
        bit_stream = self.encode_data()
        # Generate the error correction codewords at each level of precision
        (self.ec_high_prec, self.ec_med_prec, self.ec_low_prec) = self.generate_error_correction_codewords(10, 5, 3)
        # Restructure the data
        self.restructure_data()
        (red_data, green_data, blue_data) = self.split_data()
        # We now need to build the QR code for each colour channel
        red_qr_code = self.build_qr_code(red_data)
        green_qr_code = self.build_qr_code(green_data)
        blue_qr_code = self.build_qr_code(blue_data)

    def build_qr_code(self, data):
        #We need to build a QR code from scratch

            

    def save(self, save_path):
        NotImplemented

    def restructure_data(self):
        separator = bytearray([0xFF, 0xFF, 0xFF, 0xFF])
        
        #Join the data blocks together
        original_data = b''.join([data_block for data_block in self.data])
        #Join the error correction blocks together
        data_with_codewords = b''.join([
            original_data,
            separator,
            self.ec_high_prec,
            separator,
            self.ec_med_prec,
            separator,
            self.ec_low_prec
        ])
        self.data = data_with_codewords

    def float_to_bytes(self, float, precision="double"):
        format_char = "d" if precision == "double" else "f" if precision=="single" else "e" #'e' for half precision 
        return bytearray(struct.pack(format_char, float))
    
    def bytes_to_float(self, byte_array, precision="double"):
        format_char = "d" if precision == "double" else "f" if precision=="single" else "e" #'e' for half precision 
        return struct.unpack(format_char, byte_array)[0]

    def generate_error_correction_codewords(self, inner_precision, outer_precision, outer_outer_precision):
        rs_inner = RSCodec(inner_precision)
        rs_outer = RSCodec(outer_precision)
        rs_outer_outer = RSCodec(outer_outer_precision)

        #Encode each float with high-precision error correction
        encoded_floats = [[rs_inner.encode(self.float_to_bytes(float, "double")) for float in data_block] for data_block in self.data]

        #Encode each float array with a lower precision error correction
        low_precision_float_array = self.data.astype(np.float32)
        encoded_low_precision = [rs_outer.encode(b''.join(self.float_to_bytes(float, precision='single') for float in float_array)) for float_array in low_precision_float_array]

        #Encode the float array with lowest precision
        lowest_precision_float_array = self.data.astype(np.float16)
        encoded_lowest_precision = rs_outer_outer.encode(b''.join(self.float_to_bytes(float, precision='half') for float_array in lowest_precision_float_array for f in float_array))

        return encoded_floats, encoded_low_precision, encoded_lowest_precision
            
    

    def split_data(self):
        """
        This function splits the data into three equal parts.
        """
        # Splits data into 3 equal parts
        red_data = bytearray()
        green_data = bytearray()
        blue_data = bytearray()

        for i in range(0,len(self.data)):
            if i % 3 == 0:
                red_data += self.data[i]
            elif i % 3 == 1:
                green_data += self.data[i]
            else:
                blue_data += self.data[i]

        return red_data, green_data, blue_data

    def structure_final_message(self):
        NotImplemented

    def place_modules(self):
        NotImplemented
    def apply_data_masking(self):
        NotImplemented

    def add_format_and_version_info(self):
        NotImplemented

    def cvt_matrix_to_img(self, foreground_colour, background_colour):
        return NotImplemented




