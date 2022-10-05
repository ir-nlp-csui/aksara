__author__ = 'max'

import re
MAX_CHAR_LENGTH = 45
NUM_CHAR_PAD = 2

# Regular expressions used to normalize digits.
DIGIT_RE = re.compile(r"\d")

# discard secondary labels
def get_main_deplabel(label):
    return label.split(":")[0]
