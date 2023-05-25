import sys
sys.path.append("../# HK")
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import HK_func_file_folder_control as HK


def plot_heatmap(data, filename, savedir, show = False, grid = False, save = True, vmin = None, vmax = None):
    colormap = plt.cm.OrRd
    # 1. 기본 스타일 설정
    fig = plt.figure(figsize=(16, 10), dpi=100)  # 주의 : 총해상도(pixel이자 size와 같은 말) = dpi * figsize
    # plt.style.use("default") # 참고 : 그래프의 스타일, 'default'도 가능, heatmap에서는 다 가려져셔 티가 안남.
    # plt.rcParams['font.size'] = 25 # 주의 : 앞으로 나오는 글자들에 대해 크기 적용함


    # 아래는 작동하지 않지만 원인은 아직 모르는 것들
    ##추정 plt에서만 작동, sns라서 작동하지 않는듯
    ################################################################################

    # plt.rcParams['font.family'] = 'Malgun Gothic' # 참고 : rc = Runtime Configuration Parameters
    # plt.rcParams[figure.figsize] = (5, 5)  # 참고 : Heatmap의 가로, 세로 길이 !
    # fig.rcParams["fig.figsize"] = (10, 10)
    # plt.rcParams['figure.dpi'] = 5 # pixels(dots) per inches

    ################################################################################


    # # 2. 그래프 그리기
    # plt.plot(data) # 테스트용
    # sns.set(font_scale=10) # Heatmap 옆의 scale size 조정
    sns.set(font_scale=2)
    ax = sns.heatmap(data, cmap=colormap, annot=True, vmin=vmin, vmax=vmax)  # 참고 : annot = 숫자 출력, annot_kws = Heatmap 안의 수치 size, ex ) annot_kws={"size": 20}
    title = filename[:-4].split("_")
    plt.title("//".join(title))
    # plt.savefig(fname=f'{savedir}\\{title}', dpi=500, bbox_inches='tight')

    # ax = sns.heatmap(data, annot=True, annot_kws={"size": 20}, vmin=vmin,
    #                  vmax=vmax)  # 참고 : annot =    숫자 출력, annot_kws = Heatmap 안의 수치 size
    # plt.title(title)
    # plt.savefig(fname=f'{savedir}\\{title}', dpi=500, bbox_inches='tight')
    # ax.set_xticklabels(fontsize=

    # plt.xlabel("Frequency(hz)")
    # plt.ylabel("Amplitude(°)")
    # plt.ylabel("Amplitude(mm)")

    # 조건들
    if show:
        plt.show()
    if grid:
        plt.grid()
    if save:
        plt.savefig(fname=f'{savedir}\\{filename}', dpi=500, bbox_inches='tight')
    plt.close()

#파일 확인
file = HK.select_file(init_dir="D:\# Shared_Folder_HDD\\tmp\data")
savedir = HK.select_folder_location(init_dir="D:\# Shared_Folder_HDD\\tmp\data")
print(os.path.exists(file))
data = pd.read_excel(file)
DF = pd.DataFrame()
for roi in data["ROI"].unique():
    tmp = data[data["ROI"] == roi]
    if 1:
        for mode in tmp["mode"].unique():
            tmp2 = tmp[tmp["mode"] == mode]
            if 1:
                for phone in tmp2["Phone"].unique():
                    tmp3 = tmp2[tmp2["Phone"] == phone]
                    # tmp3 = tmp3[tmp3["Frequency(Hz)"] != "1Hz"]
                    # tmp3["Normalized Pixel Movement(All)"] = tmp3["Normalized Pixel Movement"] / tmp["Normalized Pixel Movement"].max() * 100
                    tmp3 = tmp3.pivot(index="+-Angle", columns="Frequency(Hz)", values="Normalized Pxls")
                    tmp3 = tmp3.sort_index(ascending=False)
                    plot_heatmap(data=tmp3, filename=f'Yaw-pitch _ {phone} _ {mode} _ {roi}.png', savedir=savedir, vmin=0, vmax=40)
            if 0:
                tmp3 = tmp2.pivot(index="Amplitude(deg)", columns="Frequency(Hz)", values="보정률(백분율)")
                tmp3 = tmp3.sort_index(ascending=False)
                plot_heatmap(data=tmp3, filename=f'Yaw&Pitch_{phone}_{mode}.png', savedir=savedir)

            if 0:
                for roi in tmp2["ROI"].unique():
                    tmp3 = tmp2[tmp2["ROI"] == roi]
                    # tmp4 = tmp3.pivot(index="Amplitude(deg)", columns="Frequency(Hz)", values="Pixel Movement")
                    # tmp4 = tmp4.sort_index(ascending=False)
                    # plot_heatmap(data=tmp4, filename=f'Yaw-pitch _ {phone} _ {mode} _ {roi}_Pixel Movement.png', savedir=savedir, vmin=tmp3["Pixel Movement"].min(), vmax=tmp3["Pixel Movement"].max())

                    tmp5 = tmp3.pivot(index="Amplitude(deg)", columns="Frequency(Hz)", values="Normalized Pixel Movement(All)")
                    tmp5 = tmp5.sort_index(ascending=False)
                    plot_heatmap(data=tmp5, filename=f'Yaw-pitch _ {phone} _ {mode} _ {roi}_Normalized Pixel Movement.png', savedir=savedir, vmin=0, vmax=100)
            if 0:

                tmp3 = tmp2[tmp2["ROI"] == "C"]
                tmp5 = tmp3.pivot(index="Amplitude(deg)", columns="Frequency(Hz)", values="Normalized Pixel Movement(All)")
                tmp5 = tmp5.sort_index(ascending=False)
                plot_heatmap(data=tmp5, filename=f'Yaw-pitch _ {phone} _ {mode} _ C _Normalized Pixel Movement.png', savedir=savedir, vmin=0, vmax=100)


            if 0:

                tmp3 = tmp2
                tmp5 = tmp3.pivot(index="Amplitude(deg)", columns="Frequency(Hz)", values="Normalized Pixel Movement(All)")
                tmp5 = tmp5.sort_index(ascending=False)
                plot_heatmap(data=tmp5, filename=f'Yaw-pitch _ {phone} _ {mode} _ RT _Normalized Pixel Movement.png', savedir=savedir, vmin=0, vmax=100)

    if 0:
        tmp["ROI 별 Normalization"] = tmp["Devide by Patch size(normalization)"] / tmp["Devide by Patch size(normalization)"].max() * 100
        DF = pd.concat([DF, tmp], axis=0)
# DF.to_excel(f'{savedir}/Summary.xlsx')
