"""This function loads raw data and rotate flop to have them in ImageJ format.

Input is the file path, output is the image matrix.
"""

import numpy as np
import czifile


class RawDataLoader:
    """Only class, does all the job."""
    def __init__(self, file_path):

        ff              =  np.rot90(np.squeeze(czifile.imread(file_path)), axes=(1, 2))[:, ::-1]     # transform the stack to adapt to the imageJ visualization standard
        a               =  czifile.CziFile(file_path)                # read info about pixel size
        b               =  a.metadata()
        start           =  b.find("ScalingX")
        end             =  b[start + 9:].find("ScalingX")

        self.pix_sizeX  =  float(b[start + 9:start + 7 + end]) * 1000000
        self.dorsal     =  ff[0]
        self.snail      =  ff[1]
        self.dapi       =  ff[2]



