
import os
import json
import torch

from .neuronlp2.io import  conllx_data
from .neuronlp2.io_multi import  get_word_index_with_spec
from .neuronlp2.models import BiRecurrentConvBiAffine
from .model_proxy import ModelProxy

ROOT_CHAR = "_ROOT_CHAR"
ROOT_POS = "_ROOT_POS"
ROOT = "_ROOT"

class DependencyParser: 
    def __init__(self, model_name='FR_GSD-ID_CSUI'):
        current_dir = os.path.dirname(__file__)
        alphabet_path = os.path.join(current_dir, "alphabets")
        self.word_alphabet, self.char_alphabet, self.pos_alphabet, self.type_alphabet, _ = conllx_data.create_alphabets(alphabet_path,
            None, data_paths=[None, None], max_vocabulary_size=50000, embedd_dict=None)
        
        model_dir = os.path.join(current_dir, ".pretrained_model")
        if not os.path.isdir(model_dir): 
            os.makedirs(model_dir)
        
        def load_model_arguments_from_json():
            file_handle = open(arg_path, 'r')
            arguments = json.load(file_handle)
            file_handle.close()
            return arguments['args'], arguments['kwargs']
        
        self.model_path = os.path.join(model_dir, model_name)
        self.model_path += '.pt'
        arg_path = self.model_path + '.arg.json'
        
        if not os.path.exists(self.model_path) or not os.path.exists(arg_path):
            ModelProxy.download_model(model_name)

        args, kwargs = load_model_arguments_from_json()
        self.model = BiRecurrentConvBiAffine(use_gpu=False, *args, **kwargs)
        
        self.model.load_state_dict(torch.load(self.model_path))
    
    def parse_rows(self, rows):
        modified_rows = rows.copy()
        heads_pred, types_pred = self.predict(rows)
        
        i = 1
        for row in modified_rows:
            if (row[0].isnumeric()):
                row[6] = str(heads_pred[i])
                row[7] = self.type_alphabet.get_instance(types_pred[i])
                i += 1
        return modified_rows

    def predict(self, rows):
        self.model.cpu()
        self.model.eval()

        words, chars, postags = self.convert_to_tensor(rows)
        mask = torch.tensor([[1 for i in range(words.shape[1])]])
        length = torch.tensor([words.shape[1]]) 

        temp_heads_pred, temp_types_pred = self.model.decode_mst(words, chars, postags, mask=mask, length=length,
                                        leading_symbolic=conllx_data.NUM_SYMBOLIC_TAGS)

        heads_pred = temp_heads_pred[0, :]
        types_pred = temp_types_pred[0, :]
        
        return heads_pred, types_pred
    
    def convert_to_tensor(self, rows):
        words = []
        chars = []
        postags = []
        max_char_len = 0

        for row in rows:
            if max_char_len < len(row[1]):
                max_char_len = len(row[1])

        words.append(self.word_alphabet.get_index(ROOT))
        temp_char = [self.char_alphabet.get_index(ROOT_CHAR)]
        for padding in range(max_char_len - 1):
            temp_char.append(1)
        chars.append(temp_char)
        postags.append(self.pos_alphabet.get_index(ROOT_POS))

        for row in rows:
            if(row[0].isnumeric()):
                words.append(get_word_index_with_spec(self.word_alphabet, row[1], 'id'))
                temp_char = []
                for char in row[1]:
                    temp_char.append(self.char_alphabet.get_index(char))
                for padding in range(max_char_len - len(row[1])):
                    temp_char.append(1)
                chars.append(temp_char)
                postags.append(self.pos_alphabet.get_index(row[3]))
        
        return torch.tensor([words]), torch.tensor([chars]), torch.tensor([postags])


