import torch # Importing the pytorch module
import numpy as np # Importing the numpy module


def main():
    linearization_point = np.array([[[0.3934939439],[0.020323020],[1.4843834334], [0.9102010129]],
                                    [[1.8884432323232],[0.2032030203],[1.09102323231],[0.573747347374]],
                                    [[2.],[0.],[1.],[0.]]], dtype=np.float64)
    
    linearization_point = torch.from_numpy(linearization_point)
    # Variable to factor messages
    message_mean_1 = np.array([[[[0.100101011010],[0.4747474774],[1.343434343434],[0.354453232]],
                              [[0.2323232323232],[0.0000000000],[1.888888888888],[0.333333453232]]],
                             [[[1.2202020202020],[0.20302320320302302],[1.44532323223],[0.2323253432232]],
                              [[1.023020320302],[0.737234727323],[1.034030430203102],[0.3848382812912]]],
                             [[[2.023020203020312],[0.85838293232],[1.0120102011212],[0.8382382838382832]],
                              [[2.],[0.],[1.],[0.]]]], dtype=np.float64)
    
    message_precision_1 = np.array([[[[ 1.9120100121,  0.38483483823,  0.344343434343],
                                    [ 0.0000,  1.0000,  0.0000],
                                    [ 0.0000,  0.0000,  1.0000]],
                                   [[ 1.0000,  0.0000,  0.0000],
                                    [ 0.0000,  1.0000,  0.0000],
                                    [ 0.0000,  0.0000,  1.0000]]],
                                  [[[ 0.0000,  0.0000,  0.0000],
                                    [ 0.0000,  0.0000,  0.0000],
                                    [ 0.0000,  0.0000,  0.0000]],
                                   [[ 1.0000,  0.0000,  0.0000],
                                    [ 0.0000,  1.0000, -1.0000],
                                    [ 0.0000, -1.0000,  2.0000]]],
                                  [[[ 0.0000,  0.0000,  0.0000],
                                    [ 0.0000,  0.0000,  0.0000],
                                    [ 0.0000,  0.0000,  0.0000]],
                                   [[ 1.0000,  0.0000,  0.0000],
                                    [ 0.0000,  1.0000, -2.0000],
                                    [ 0.0000, -2.0000,  5.0000]]]], dtype=np.float64)
    message_precision_1 = torch.from_numpy(message_precision_1)
    
    # Factor to variable messages
    message_mean_2 = np.array([[[[0.],[0.],[1.],[0.]],
                                [[0.],[0.],[1.],[0.]]],
                               [[[1.],[0.],[1.],[0.]],
                                [[1.],[0.],[1.],[0.]]],
                               [[[2.],[0.],[1.],[0.]],
                                [[0.],[0.],[1.],[0.]]]], dtype=np.float64)
    message_mean_2 = torch.from_numpy(message_mean_2)
    
    message_precision_2 = np.array([[[[ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000]],
                                     [[ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000]]],
                                    [[[ 1.0000,  0.0000,  0.0000],
                                      [ 0.0000,  1.0000, -1.0000],
                                      [ 0.0000, -1.0000,  2.0000]],
                                     [[ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000]]],
                                    [[[ 1.0000,  0.0000,  0.0000],
                                      [ 0.0000,  1.0000, -2.0000],
                                      [ 0.0000, -2.0000,  5.0000]],
                                     [[ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000],
                                      [ 0.0000,  0.0000,  0.0000]]]])
    message_precision_2 = torch.from_numpy(message_precision_2)

    variable_to_factor_messages = {"message mean": message_mean_1, "message precision": message_precision_1}
    factor_to_variable_messages = {"message mean": message_mean_2, "message precision": message_precision_2}

    data = {"linearization point": linearization_point, "variable to factor messages": variable_to_factor_messages, "factor to variable messages": factor_to_variable_messages}

    torch.save(data, "example_messages.pt")

if __name__ == "__main__":
    main()

