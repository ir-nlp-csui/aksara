#!/usr/bin/python3

import aksara
import os

current_dir,_ = os.path.split(os.path.realpath(__file__))

BIN_FILE = "bin/aksara@v1.2.0.bin"

aksara.create_args_parser(os.path.join(current_dir, BIN_FILE))