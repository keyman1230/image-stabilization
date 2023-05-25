import sys
sys.path.append("./# HK")
sys.path.append("./# 분석결과 Edit")
sys.path.append("./# 분석 결과 merge 및 계산")
sys.path.append("./# Heatmap")

import os
import pandas as pd


import HK_func_file_folder_control as HK
import Edit_Excel as EE
import Calculation_n_Merge as CM
import Draw_Heatmap as DH

################# USER INPUT #########################
#
#
#
#
#
OIS_result_dir = "D:\# Shared_Folder_HDD\# Image Database\# Functional Evaluation\# OIS"
patch_size = 60
#
#
#
#
#
#
#
#
#
##########################################


########## 1. OIS 결과 수정

# Excel File list 확보
filelist = HK.make_filelist(HK.select_folder_location(init_dir=OIS_result_dir), subdir=False, list_filetype=[".xlsx"])

# 각각의 파일들에 대해서,
for path in filelist:
    savefolder = os.path.dirname(path) #
    savefilename = os.path.basename(path).split("_")[3]
    df = pd.read_excel(io=path, sheet_name=0)
    df = EE.Delete_columns(df)
    df = EE.Delete_noise(Input_DF=df, patch_size_threshold=patch_size)
    df = EE.Rename_ROI(df)
    df.to_excel(f"{savefolder}//{savefilename}.xlsx")

########## 2. 계산 및 merge excel
