"""
Position feed-forward network from "Attention is All You Need"
"""

import torch.nn as nn

from .util_class import LayerNorm


class PositionwiseFeedForward(nn.Module):
    """ A two-layer Feed-Forward-Network with residual layer norm.
        Args:
            d_model (int): the size of input for the first-layer of the FFN.
            d_ff (int): the hidden layer size of the second-layer
                              of the FNN.
            dropout (float): dropout probability(0-1.0).
    """

    def __init__(self, d_model, d_ff, relu_drop=0.1, res_drop=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.layer_norm = LayerNorm(d_model)
        self.relu_dropout = nn.Dropout(relu_drop)
        self.relu = nn.ReLU()
        self.residual_dropout = nn.Dropout(res_drop)

    def forward(self, x):
        """
        Layer definition.
        Args:
            input: [ batch_size, input_len, model_dim ]
        Returns:
            output: [ batch_size, input_len, model_dim ]
        """
        inter = self.relu_dropout(self.relu(self.w_1(self.layer_norm(x))))
        output = self.residual_dropout(self.w_2(inter))
        return output + x
