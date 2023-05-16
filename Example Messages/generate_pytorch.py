import torch # Importing the pytorch module
import numpy as np # Importing the numpy module


def main():
    linearization_point = np.array([[[0.],[0.],[1.], [0.]],
                                    [[1.],[0.],[1.],[0.]],
                                    [[2.],[0.],[1.],[0.]]], dtype=np.float64)
    
    linearization_point = torch.from_numpy(linearization_point)
    # Variable to factor messages
    message_mean_1 = np.array([[[[0.],[0.],[1.],[0.]],
                              [[0.],[0.],[1.],[0.]]],
                             [[[1.],[0.],[1.],[0.]],
                              [[1.],[0.],[1.],[0.]]],
                             [[[2.],[0.],[1.],[0.]],
                              [[2.],[0.],[1.],[0.]]]], dtype=np.float64)
    
    message_precision_1 = np.array([[[[ 1.0000,  0.0000,  0.0000],
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

