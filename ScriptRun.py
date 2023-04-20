"""This script estimate the dorsal concentration inside and outside nuclei recursivly
on a bunch of files.

input is the list of file names, output excel filewith results.

developer contact: antonio.trullo@cnrs.igmm.fr
first version 15 Apr 2023
"""

import xlsxwriter
from PyQt5 import QtWidgets

import RawDataLoader
import NucleiDetector


darks_path  =  QtWidgets.QFileDialog.getOpenFileNames(None, "Select raw data file to analyse...", filter="*.lsm *.czi *.tif *.lif")[0]

dark_info   =  []
for dark_path in darks_path:
    print("slkdfjlk")
    raw_data   =  RawDataLoader.RawDataLoader(dark_path)
    bff        =  NucleiDetector.NucleiDetector(raw_data.dapi, raw_data.dorsal)
    dark_info.append([dark_path[dark_path.rfind('/') + 1:], bff.nucs_ints, bff.bckg_ints])


lights_path  =  QtWidgets.QFileDialog.getOpenFileNames(None, "Select raw data file to analyse...", filter="*.lsm *.czi *.tif *.lif")[0]
light_info   =  []
for light_path in lights_path:
    print("slkdfjlk")
    raw_data   =  RawDataLoader.RawDataLoader(light_path)
    bff        =  NucleiDetector.NucleiDetector(raw_data.dapi, raw_data.dorsal)
    light_info.append([light_path[light_path.rfind('/') + 1:], bff.nucs_ints, bff.bckg_ints])

book      =  xlsxwriter.Workbook("/home/atrullo/Dropbox/Virginia_Anto/Dorsal LEXY/FOR_ANTO_FIXEDdl/Results.xlsx")
sh_dark   =  book.add_worksheet("Dark")
sh_light  =  book.add_worksheet("Light")

sh_dark.write(0, 0, "File Name")
sh_dark.write(0, 1, "Internal Ints")
sh_dark.write(0, 2, "External Ints")
sh_dark.write(0, 3, "Ratio (Int/ext)")
sh_light.write(0, 0, "File Name")
sh_light.write(0, 1, "Internal Ints")
sh_light.write(0, 2, "External Ints")
sh_light.write(0, 3, "Ratio (Int/ext)")

for cnt1, infdark in enumerate(dark_info):
    sh_dark.write(cnt1 + 1, 0, infdark[0])
    sh_dark.write(cnt1 + 1, 1, infdark[1])
    sh_dark.write(cnt1 + 1, 2, infdark[2])
    sh_dark.write(cnt1 + 1, 3, infdark[1] / infdark[2])

for cnt2, inflight in enumerate(light_info):
    sh_light.write(cnt2 + 1, 0, inflight[0])
    sh_light.write(cnt2 + 1, 1, inflight[1])
    sh_light.write(cnt2 + 1, 2, inflight[2])
    sh_light.write(cnt2 + 1, 3, inflight[1] / inflight[2])

book.close()