from data_formatter import DataFormatter

class QRCode:

    def __init__(self, data_path):
        self.data = DataFormatter(data_path)

    def generate_qr_code(self):
        """
        This function prepares the data for encoding.
        """
        # Perform data compression on the data
        self.data.compress()

        # Format the data into codewords
        data_int = self.data.data_int.as_codewords()
        data_msb = self.data.data_msb.as_codewords()
        data_lsb = self.data.data_lsb.as_codewords()
        # Generate error correction codewords on the data
        self.data.generate_error_correction()
        ecdata_int = self.data.ecdata_int
        ecdata_msb = self.data.ecdata_msb
        ecdata_lsb = self.data.ecdata_lsb
        
        # Combine the data and error correction codewords
        data_int.append(ecdata_int)
        data_msb.append(ecdata_msb)
        data_lsb.append(ecdata_lsb)
        
        # Interleave the data
        data = self.interleave_data(data_int, data_msb, data_lsb)
        print(len(data))
        # Calculate the required size of the code required to fit the data

        # Generate meta data

        # Build matrix of the required size

        # Fill in the matrix with recognisable patterns

        # Fill in matrix with the meta data

        # Fill in matrix with the main data

        # Convert matrix to QR code

        # Return QR code
        
    def interleave_data(self, data_int, data_msb, data_lsb):
        """
            This function interleaves all the codewords into a single array
        """
        # Calculate the maximum length of the 3 data parts
        max_length = max(len(data_int), len(data_msb), len(data_lsb))
        
        # Pad the data parts with 0s to make them all the same length
        data_int += [0] * (max_length - len(data_int))
        data_msb += [0] * (max_length - len(data_msb))
        data_lsb += [0] * (max_length - len(data_lsb))
        
        # Interleave the data parts 
        interleaved_data = []
        for i in range(max_length):
            interleaved_data.append(data_int[i])
            interleaved_data.append(data_msb[i])
            interleaved_data.append(data_lsb[i])
        
        # Remove trailing 0s
        while interleaved_data and interleaved_data[-1] == 0:
            interleaved_data.pop()
            
        return interleaved_data


if __name__ == "__main__":
    qr_code = QRCode("example_window.json")
    qr_code.generate_qr_code()