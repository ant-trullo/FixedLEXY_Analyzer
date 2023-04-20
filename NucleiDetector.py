"""This function segments 2D dapi nuclei in single time frame,
defines a background region just around and measure the intensity
of nuclei and background in the dorsal channel.

Input is the numpy image matrix.
"""


import numpy as np
from skimage.filters import gaussian, threshold_otsu
from skimage.morphology import label, remove_small_objects
from skimage.segmentation import expand_labels

# intensity must be taken dorsal (use this mask) and write an excell file with ratio and all the info.


class NucleiDetector:
    """Only class, does all the job."""
    def __init__(self, dapi, dorsal):

        dapi_f     =  gaussian(dapi, 5)                                             # pre-smoothing with a very high kernel
        val        =  threshold_otsu(dapi_f ** 2)                                   # otsu threshold on the square of the matrix (non-linear transformation is required for the inhomogeneity of the intensity)
        ratio      =  []                                                            # initiallize the ratio list
        for ii in range(1, 10):                                                     # 9 different threshold will be tried, for each threhsold multiplier value
            ratio.append([(dapi_f ** 2 > val * 0.1 * ii).sum() / dapi.size, ii])    # append the ratio between number of white points and the matrix size, plus the threshold multiplier

        ratio      =  np.asarray(ratio)                                             # make it np array, easier to deal with
        oo         =  np.argmin(np.abs(ratio[:, 0] - 0.1))                          # for those data nuclei are around the 10% of the image, so we search the ratio closer to .1
        nucs       =  dapi_f ** 2 > val * 0.1 * ratio[oo, 1]                        # threshold with the proper multiplier
        nucs_lbls  =  label(nucs)                                                   # label in order to ...
        nucs_fin   =  np.sign(remove_small_objects(nucs_lbls, 1000))                # ... remove small objects
        nucs_bckg  =  expand_labels(nucs_fin, distance=55) - nucs_fin               # define mask for the background, just around the nuclei

        nucs_ints  =  np.sum(nucs_fin * dorsal) / nucs_fin.sum()                    # dorsal average intensty in the nuclei
        bckg_ints  =  np.sum((nucs_bckg * dorsal)) / nucs_bckg.sum()                # dorsal average intensity around nuclei

        self.nucs_fin   =  nucs_fin
        self.nucs_bckg  =  nucs_bckg
        self.nucs_ints  =  nucs_ints
        self.bckg_ints  =  bckg_ints
