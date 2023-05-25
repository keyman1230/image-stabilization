import sys
sys.path.append('../# HK')

from HK_func_file_folder_control import *
# from HK_func_image_movie_file_control import *
import pandas as pd

if __name__ == "__main__":
    f = select_file(init_dir = "D:\# Shared_Folder_HDD\# Python_Code_and_Tool\# OIS Analyzer GUI\SAMPLE\_Result\Objective_X-X-X-X-X_X50 Pro-x1.0-Default-Photo-Preview_EIS OFF-Pitch-10.0deg-1Hz_V2005A 2023-05-18 11-53-56_Crop-104-74-867-505")
    df = pd.read_excel(f)
    print()
    for frameno in range(1, df.Frame_No.max()+1):
        patches = df[df.Frame_No == frameno]
        if patches.__len__() != 9:
            print(frameno)