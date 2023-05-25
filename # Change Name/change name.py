import os.path
import sys
sys.path.append("../# HK")
import HK_func_file_folder_control as HK

import pandas as pd

import shutil

def make_new_name(df):
    ['Chart', 'Light', 'Color T', 'Luminance', 'Measured T', 'Measured L',
     'Camera', 'Magnitude', 'Camera Apps', 'Capture Mode', 'IS mode',
     'Vibration', 'Amp', 'Freq', 'Original name']

    Chart = df['Chart']
    Light = df['Light'] + '-' + df['Color T'] + '-' + df['Luminance'] + '-' + df['Measured T'] + '-' + df['Measured L']
    Phone = df['Camera'] + '-' + df['Magnitude'] + '-' + df['Camera Apps'] + '-' + df['Capture Mode']
    Vibration = df['IS mode'] + '-' + df['Vibration'] + '-' +  df['Amp'] + '-' +  df['Freq']
    newname = Chart + "_" + Light + "_" + Phone + "_" + Vibration
    df["New name"] = newname
    return df

if __name__ == "__main__":
    # 1. Load
    workdir = HK.select_folder_location(init_dir="D:\# Shared_Folder_HDD\# Image Database\# Image Quality\# 2023\OIS 재촬영\Galaxy S23 Ultra\EIS OFF\Sub")
    file_list = HK.make_filelist(target_dir=workdir, subdir=False, list_filetype=[".mp4",".mov" ]) # 이름을 바꿔야 할 파일 리스트
    name_file = HK.select_file(init_dir="D:\# Shared_Folder_HDD\# Python_Code_and_Tool\# OIS Analyzer GUI\# Change Name")
    name_df = pd.read_excel(name_file)

    ##  길이 검사
    if len(file_list) != len(name_df):
        print("바꾸고자하는 파일 개수랑 이름의 개수가 일치하지 않습니다. 확인해주세요 !!")
        exit()

    # 2. 이름 매칭
    name_df = make_new_name(name_df)
    name_df["Original name"] = file_list

    # 3. 복사
    for i in range(len(name_df)):
        ori = name_df.iloc[i]["Original name"] # 기존 이름
        dirname = os.path.dirname(ori) # 폴더 위치
        base = os.path.basename(ori)
        # ext = os.path.splitext(ori)[1] # 파일 형식

        new = f'{dirname}//{name_df.iloc[i]["New name"]}_{base}'

        shutil.copy(ori, new)


