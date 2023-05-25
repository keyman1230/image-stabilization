import sys
sys.path.append("../# HK")
import HK_func_file_folder_control as HK
import pandas as pd
import os
import json
import numpy as np


def make_default_setting_file():
    iterables = [
                 ["iPhone 14 Pro", "Galaxy S23 Ultra", "X50 Pro", "Find X5 Pro"],
                 ["EIS", "OIS"]
                ]
    index = pd.MultiIndex.from_product(iterables=iterables, names=["Phone", "Mode"])
    patch_size = [
        [60, 70], # 14 Pro       // EIS // Video // Record // 안정화 향상 // 1920 x 1080
        [120, 130], # 14 Pro    // OIS // Photo // Preview // 960 x 540
        3, # S23 Ultra // EIS
        4, # S23 Ultra // OIS
        5, # X50 Pro            // EIS // Video // Record // Ultrastable x // 1920 x 1080
        6, # X50 Pro            // OIS
        7, # X5 Pro    // EIS
        8  # X5 Pro    // OIS
    ]
    Patch_size = pd.DataFrame(data=patch_size, columns=["Patch Min","Patch Max"], index=index)

    # Boundary
    ROIs = ["LT", "LB", "C", "RT", "RB"]
    iterables.append(ROIs)
    index = pd.MultiIndex.from_product(iterables=iterables, names=["Phone", "Mode", "ROI"])
    columns = ["Xmin", "Xmax", "Ymin", "Ymax"]
    data = [
        [1, 1, 1, 1],  # 14 Pro    // EIS // LT
        [1, 1, 1, 1],  # 14 Pro    // EIS // LB
        [1, 1, 1, 1],  # 14 Pro    // EIS // C
        [1, 1, 1, 1],  # 14 Pro    // EIS // RT
        [1, 1, 1, 1],  # 14 Pro    // EIS // RB

        [2, 2, 2, 2],  # 14 Pro    // OIS // LT
        [2, 2, 2, 2],  # 14 Pro    // OIS // LB
        [2, 2, 2, 2],  # 14 Pro    // OIS // C
        [2, 2, 2, 2],  # 14 Pro    // OIS // RT
        [2, 2, 2, 2],  # 14 Pro    // OIS // RB

        [3, 3, 3, 3],  # S23 Ultra // EIS // LT
        [3, 3, 3, 3],  # S23 Ultra // EIS // LB
        [3, 3, 3, 3],  # S23 Ultra // EIS // C
        [3, 3, 3, 3],  # S23 Ultra // EIS // RT
        [3, 3, 3, 3],  # S23 Ultra // EIS // RB

        [4, 4, 4, 4],  # S23 Ultra // OIS // LT
        [4, 4, 4, 4],  # S23 Ultra // OIS // LB
        [4, 4, 4, 4],  # S23 Ultra // OIS // C
        [4, 4, 4, 4],  # S23 Ultra // OIS // RT
        [4, 4, 4, 4],  # S23 Ultra // OIS // RB

        [5, 5, 5, 5],  # S23 Ultra // EIS // LT
        [5, 5, 5, 5],  # S23 Ultra // EIS // LB
        [5, 5, 5, 5],  # S23 Ultra // EIS // C
        [5, 5, 5, 5],  # S23 Ultra // EIS // RT
        [5, 5, 5, 5],  # S23 Ultra // EIS // RB

        [6, 6, 6, 6],  # S23 Ultra // OIS // LT
        [6, 6, 6, 6],  # S23 Ultra // OIS // LB
        [6, 6, 6, 6],  # S23 Ultra // OIS // C
        [6, 6, 6, 6],  # S23 Ultra // OIS // RT
        [6, 6, 6, 6],  # S23 Ultra // OIS // RB

        [7, 7, 7, 7],  # X5 Pro    // EIS // LT
        [7, 7, 7, 7],  # X5 Pro    // EIS // LB
        [7, 7, 7, 7],  # X5 Pro    // EIS // C
        [7, 7, 7, 7],  # X5 Pro    // EIS // RT
        [7, 7, 7, 7],  # X5 Pro    // EIS // RB

        [8, 8, 8, 8],  # X5 Pro    // OIS // LT
        [8, 8, 8, 8],  # X5 Pro    // OIS // LB
        [8, 8, 8, 8],  # X5 Pro    // OIS // C
        [8, 8, 8, 8],  # X5 Pro    // OIS // RT
        [8, 8, 8, 8],  # X5 Pro    // OIS // RB
    ]
    Boundary_ROI = pd.DataFrame(data=data, index=index, columns=columns)

    Settiing_Dict = {
        "Patch_size": Patch_size,
        "Boundary_ROI": Boundary_ROI
    }

    for key in Settiing_Dict.keys():
        Settiing_Dict[key].to_excel("./" + key + ".xlsx")
def Delete_columns(Input_DF):
    Input_DF.drop(["Marker_Center_X_crop", "Marker_Center_Y_crop"], axis=1, inplace=True)
    return Input_DF

def Delete_noise(Input_DF, size_min, size_max):

    Input_DF = Input_DF[(Input_DF["Marker_Width"] >= size_min) & (Input_DF["Marker_Width"] <= size_max)]
    Input_DF = Input_DF[(Input_DF["Marker_Width"] >= size_min) & (Input_DF["Marker_Width"] <= size_max)]
    # Input_DF = Input_DF[Input_DF["Frame_No"] > 800]
    return Input_DF

def Rename_ROI_eis_on(Input_DF):
    # EIS ON
    # Galaxy S23 Ultra, iPhone 14 pro
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 1000) & (Input_DF["Marker_Center_Y_full"] > 100)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 300) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 300) & (Input_DF["Marker_Center_X_full"] > 1300)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] > 1300)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_eis_off_yaw(Input_DF):
    # EIS ON
    # Galaxy S23 Ultra
    C = Input_DF[(Input_DF["Marker_Center_Y_full"] > 250) & (Input_DF["Marker_Center_Y_full"] < 350)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 150) & (Input_DF["Marker_Center_X_full"] < 400)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 150) & (Input_DF["Marker_Center_X_full"] > 600)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 400)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] > 600)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)
def Rename_ROI_eis_off_pitch(Input_DF):
    # EIS ON
    # Galaxy S23 Ultra
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 500)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 300)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 650)& (Input_DF["Marker_Center_X_full"] < 800)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 300) & (Input_DF["Marker_Center_X_full"] < 300)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 300) & (Input_DF["Marker_Center_X_full"] > 650)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_eis_off_pitch_gal(Input_DF):
    # EIS ON
    # Galaxy S23 Ultra
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 500) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 350)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 750)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 350)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] > 750)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)


def Rename_ROI_iPhone14pro_eis_off1(Input_DF):
    # 3.0도 이상 에 대해
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 350) & (Input_DF["Marker_Center_X_full"] < 450)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 250)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 580)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 350) & (Input_DF["Marker_Center_X_full"] < 250)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 350) & (Input_DF["Marker_Center_X_full"] > 580)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_iPhone14pro_eis_off2(Input_DF):
    # 3.0도 이하에 대해
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 450) & (Input_DF["Marker_Center_X_full"] < 530)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 300)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 650)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 380) & (Input_DF["Marker_Center_X_full"] < 330)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 380) & (Input_DF["Marker_Center_X_full"] > 650)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_findx5pro_eis_on(Input_DF):
    # FOR ONLY CENTER
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 1000)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 400) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 400) & (Input_DF["Marker_Center_X_full"] > 1200)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] > 1200)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_findx5pro_eis_off_yaw(Input_DF):
    # FOR ONLY CENTER
    C = Input_DF[(Input_DF["Marker_Center_Y_full"] > 250) & (Input_DF["Marker_Center_Y_full"] < 350)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 150) & (Input_DF["Marker_Center_X_full"] < 400)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 150) & (Input_DF["Marker_Center_X_full"] > 650)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 430) & (Input_DF["Marker_Center_X_full"] < 400)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 430) & (Input_DF["Marker_Center_X_full"] > 650)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)
def Rename_ROI_findx5pro_eis_off_pitch(Input_DF):
    # FOR ONLY CENTER
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 500) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 350)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 700)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 350)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] > 700)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_x50pro_eis_on(Input_DF):
    # FOR ONLY CENTER
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 1000)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 300) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 300) & (Input_DF["Marker_Center_X_full"] > 1200)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] < 600)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 800) & (Input_DF["Marker_Center_X_full"] > 1200)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Rename_ROI_x50pro_eis_off_pitch(Input_DF):
    # FOR ONLY CENTER
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 450) & (Input_DF["Marker_Center_X_full"] < 550)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 310)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 700)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 310)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] > 700)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)



def Rename_ROI_sample(Input_DF):
    # EIS ON
    # Galaxy S23 Ultra
    C = Input_DF[(Input_DF["Marker_Center_X_full"] > 600) & (Input_DF["Marker_Center_X_full"] < 700)].copy()
    C["ROI_No"] = "C"

    LT = Input_DF[(Input_DF["Marker_Center_Y_full"] > 50) & (Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] < 450)].copy()
    LT["ROI_No"] = "LT"

    RT = Input_DF[(Input_DF["Marker_Center_Y_full"] < 200) & (Input_DF["Marker_Center_X_full"] > 850)].copy()
    RT["ROI_No"] = "RT"

    LB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] < 450)].copy()
    LB["ROI_No"] = "LB"

    RB = Input_DF[(Input_DF["Marker_Center_Y_full"] > 400) & (Input_DF["Marker_Center_X_full"] > 850)].copy()
    RB["ROI_No"] = "RB"

    return pd.concat([LT, RT, C, LB, RB], axis=0)

def Edit_rawdata(io, savefolder, savefilename):
    df = pd.read_excel(io=io, sheet_name=0)
    df = Delete_columns(df)
    # Gal s23 iPhone 14 pro / eis on
    # df = Delete_noise(df, 130, 140)
    # df = Rename_ROI_eis_on(df)

    # # Gal s23  기존촬영분/ eis off
    # df = Delete_noise(df, 73, 76)
    # df = Rename_ROI_eis_off_pitch_gal(df)

    # iPhone 14 pro 기존촬영분/ eis off
    # df = Delete_noise(df, 64, 68)
    # df = Rename_ROI_eis_off_pitch(df)

    # iPhone 14 pro 3도이상 / eis off
    # df = Delete_noise(df, 60, 70)
    # df = Rename_ROI_iPhone14pro_eis_off2(df)

    # OPPO EIS on
    # df = Delete_noise(df, 115, 125)
    # df = Rename_ROI_findx5pro_eis_on(df)

    # OPPO EIS off
    # df = Delete_noise(df, 67, 71)
    # df = Rename_ROI_findx5pro_eis_off_pitch(df)


    # Vivo EIS on
    # df = Delete_noise(df, 85, 115)
    # df = Rename_ROI_x50pro_eis_on(df)

    # Vivo EIS off
    # df = Delete_noise(df, 60, 80)
    # df = Rename_ROI_x50pro_eis_off(df)

    # vivo sample test
    df = Delete_noise(df, 70, 75)
    df = Rename_ROI_x50pro_eis_off_pitch(df)



    df.to_excel(f"{savefolder}//{savefilename}.xlsx")

if __name__ == "__main__":

    # # 1. setting file 확인
    # Setting_file = "./Env_Data_Processing.json"
    # if not os.path.exists(Setting_file):
    #     make_default_setting_file()  # Default Setting파일 생성 (총 모니터링 시간 : 30s, 체크 간격 : 5s)
    #     print(
    #         "Setting파일을 찾을 수 없어, Default setting파일을 만듭니다, t_interval_seconds, t_monitoring_hours, list_monitoring_program 를 체크해주세요 ")
    #

    # 1. Excel File list 확보
    filelist = HK.make_filelist(HK.select_folder_location(init_dir="D:\# Shared_Folder_HDD\# Image Database\# Functional Evaluation\# OIS"), subdir=False, list_filetype=[".xlsx"])

    # 2. 각각의 파일들에 대해서,
    for path in filelist:
        savefolder = os.path.dirname(path)
        filenametoken =os.path.basename(path).split("_")
        savefilename = f"{filenametoken[3]}_{filenametoken[4]}" # Galaxy S22 Ultra-W-x1.0-Default-Photo-Yaw-Pitch-1.5deg-5Hz

        Edit_rawdata(io=path, savefolder=savefolder, savefilename=savefilename)

