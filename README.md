Libraries 

import sys

import queue

import operator

import numpy as np

from time import time 

from os import system

All libraries should be standard python libraries. No pip3 install statements were used to generate the code

To run the code, change the directory to proj1_dani_lerner folder. i.e.

    cd your_path/proj1_dani_lerner

The name of the python file is simply "main.py" but the terminal command has arguments.
To run all the homework assignment test cases (1 - 5, see below), type ...

    python main.py

To run any individual case, write the number next to main.py. E.g. ...

    python main.py 3             

... will run just the 3rd test case.
To run a custom grid, put the word custom after main.py. E.g ...

    python main.py custom

... will run the custom matrix. To define the matrix, change line 264 to the desired matrix
Last but not least, having any word between main.py and the number will generate a random grid of that length. E.g. ...

    python main.py random 4 

... will generate a random 4x4 sequence and run the algorithm on it.

In all the above cases, the nodePath_case_type.txt file can be found in the current directory. Please note that the text file
will overwrite each time the code is run.

The 5 test cases are shown below:

            test_case = {'1': [[1, 2, 3, 4],[ 5, 6, 0, 8], [9, 10, 7, 12], [13, 14, 11, 15]],
                         '2': [[1, 0, 3, 4],[ 5, 2, 7, 8], [9, 6, 10, 11], [13, 14, 15, 12]],
                         '3': [[0, 2, 3, 4],[ 1, 5, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
                         '4': [[5, 1, 2, 3],[ 0, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],
                         '5': [[1, 6, 2, 3],[ 9, 5, 7, 4], [0, 10, 11, 8], [13, 14, 15, 12]]}



