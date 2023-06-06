import lzma
import brotli
import zstd

class BinaryData:
    def __init__(self, data):
        #Convert data into bytes
        self.data = data

    # Returns the data as bytes
    def as_bytes(self):
        return self.data
    
    def as_bit_string(self):
        return bin(int.from_bytes(self.as_bytes(), byteorder='big'))[2:].zfill(8)
    
    # Returns the data in codeword array form
    def as_codewords(self): #TODO: Implement
        # Convert the data to bytes.
        data_bytes = self.as_bytes()
        # Split the bytes into 8-bit codewords
        codewords = [data_bytes[i:i+1] for i in range(0, len(data_bytes))]
        return codewords
    
    def compress_data(self):
        """
        This function compresses the data.
        """
        # Compress the data
        compressed_brotli = brotli.compress(self.as_bytes())
        
        print(f"Original data: {len(self.as_bytes())} bytes")
        print(f"Compressed data with Brotli: {len(compressed_brotli)} bytes")
        self.data = compressed_brotli

    def add_padding(self, target_length):
        """
        In: Target length in bytes
        This function adds padding to the data.
        """
        # Target length in bits
        target_length *= 8

        # Add padding bits until the bit string in the correct length
        bit_string = self.as_bit_string()
        while len(bit_string) < target_length:
            bit_string += '11101100' if len(bit_string) % 16 == 0 else '00010001'

        # Convert bit string back into bytes
        chunks = [bit_string[i:i+8] for i in range(0, len(bit_string), 8)]
        bytes = [int(chunk, 2).to_bytes(1, 'big') for chunk in chunks]
        self.data = bytes

    
    # Generates and appends error correction codewords to the data
    def generate_error_correction(self):
        return NotImplemented