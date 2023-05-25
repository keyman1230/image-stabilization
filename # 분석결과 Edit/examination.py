import sys
sys.path.append("../# HK")
import HK_func_file_folder_control as HK
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


def Save_overall_chart_tracking_image(df, filename, savefolder):
    # Overall Image
    fig = plt.figure(figsize=(16, 10), dpi=100)
    sns.set(font_scale=3)
    ax = sns.scatterplot(data=df, x="Marker_Center_X_full", y="Marker_Center_Y_full")  # 참고 : annot = 숫자 출력, annot_kws = Heatmap 안의 수치 size, ex ) annot_kws={"size": 20}
    plt.title(filename)
    # 조건들
    plt.savefig(fname=f'{savefolder}\\{filename}.png', dpi=500, bbox_inches='tight')
    plt.close()

    # Time plot
    for roi in df["ROI_No"].unique():
        partial = df[df["ROI_No"] == roi]
        fig, ax = plt.subplots(nrows=2)
        sns.set(font_scale=1)
        sns.scatterplot(data=partial, x="Frame_No",
                             y="Marker_Center_Y_full", ax=ax[0])  # 참고 : annot = 숫자 출력, annot_kws = Heatmap 안의 수치 size, ex ) annot_kws={"size": 20}
        sns.scatterplot(data=partial, x="Frame_No",
                             y="Marker_Center_X_full", ax=ax[1])  # 참고 : annot = 숫자 출력, annot_kws = Heatmap 안의 수치 size, ex ) annot_kws={"size": 20}

        # plt.title(f'{filename}//{roi}')
        # 조건들
        plt.savefig(fname=f'{savefolder}\\{filename}_{roi}.png', dpi=500, bbox_inches='tight')
        plt.close()

    # df.to_excel(f"{savefolder}//{savefilename}.xlsx")
    return True




if __name__ == "__main__":

    # 1. Excel File list 확보
    filelist = HK.make_filelist(HK.select_folder_location(init_dir="D:\# Shared_Folder_HDD\# Image Database\# Functional Evaluation\# OIS"), subdir=False, list_filetype=[".xlsx"])

    # 2. 각각의 파일들에 대해서,
    DF = pd.DataFrame()
    for path in filelist:
        savefolder = os.path.dirname(path)
        savefilename = os.path.splitext(os.path.basename(path))[0] # Galaxy S22 Ultra-W-x1.0-Default-Photo_Yaw-Pitch-1.5deg-5Hz
        bigtoken = savefilename.split("_")
        token1 = bigtoken[0].split("-")
        token2 = bigtoken[1].split("-")
        phone = token1[0]
        vibration = token2[0]
        angle = token2[-2]
        frequency = token2[-1]

        df = pd.read_excel(io=path, sheet_name=0)
        df["phone"] = phone
        df["angle"] = angle
        df["frequency"] = frequency

        DF = pd.concat([DF, df], axis=0)
        Save_overall_chart_tracking_image(df=df, savefolder=savefolder,filename=savefilename)
    DF.to_excel(f'{savefolder}/EIS OFF rawdata.xlsx')
