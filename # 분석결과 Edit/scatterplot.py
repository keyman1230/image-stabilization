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
    ax = sns.scatterplot(data=df, x="Marker_Center_X_full(normalized)", y="Marker_Center_Y_full(normalized)", hue="phone")  # 참고 : annot = 숫자 출력, annot_kws = Heatmap 안의 수치 size, ex ) annot_kws={"size": 20}
    plt.title(filename)
    # 조건들
    plt.savefig(fname=f'{savefolder}\\{filename}.png', dpi=500, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    file = HK.select_file(init_dir="D:\# Shared_Folder_HDD\\tmp\data")
    savedir = HK.select_folder_location(init_dir="D:\# Shared_Folder_HDD\\tmp\data")
    print(os.path.exists(file))

    # for mode in ["EIS ON","EIS OFF"]:
    DF = pd.DataFrame()
    for mode in ["EIS OFF"]:
        data = pd.read_excel(file, sheet_name=mode)
        for angle in data["angle"].unique():
            tmp = data[data["angle"] == angle]
            for frequency in tmp["frequency"].unique():
                tmp2 = tmp[tmp["frequency"] == frequency]
                # for phone in tmp2["phone"].unique():
                    # ref = tmp2[tmp2["phone"] == "Galaxy S23 Ultra"]["Marker_Width"].mean()
                    # tmp3 = tmp2[tmp2["phone"] == phone]
                    # tmp3["Marker_Center_X_full(normalized)"] = tmp3["Marker_Center_X_full"] * ref / tmp3["Marker_Width"].mean()
                    # tmp3["Marker_Center_Y_full(normalized)"] = tmp3["Marker_Center_Y_full"] * ref / tmp3["Marker_Width"].mean()
                    # DF = pd.concat([DF, tmp3], axis=0)
    # DF.to_excel(f"{savedir}//Summary_normalized.xlsx")
                Save_overall_chart_tracking_image(tmp2, filename=f"{mode}_{angle}_{frequency}", savefolder=savedir)