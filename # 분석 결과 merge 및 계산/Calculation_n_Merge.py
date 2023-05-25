
## 0. 각 폰의 데이터 만들어주는 함수
def Fill_phone_spec(phone_name, pixel_size_um, diagonal_pixelN, exif_fl_mm, converted_pixel_size_um):
    tmpdict = {}
    tmpdict["pixel size(um)"] = pixel_size_um
    tmpdict["diagonal pixel#"] = diagonal_pixelN
    sensor_diagonal_size = pixel_size_um * diagonal_pixelN / 1000
    tmpdict["sensor diagonal size(mm)"] = sensor_diagonal_size
    crop_factor = 43 / sensor_diagonal_size
    tmpdict["crop factor"] = crop_factor
    tmpdict["35mm fl"] = exif_fl_mm
    tmpdict["fl"] = exif_fl_mm / crop_factor
    tmpdict["converted_pixel_size(um)"] = converted_pixel_size_um

    phone_spec[phone_name] = tmpdict
    print(phone_spec)
    return 0


# roi 별
## 1. 픽셀 떨림양 계산
def Cal_pixel_movement():
    pass

## 2. SR(db)계산
def Cal_SR_db():
    pass

## 3. 백분율 계산
def Cal_percentage():
    pass


if __name__ == "__main__":
    import sys
    sys.path.append("../# HK")
    import HK_func_file_folder_control as HK
    import pandas as pd
    import numpy as np
    import os
    from math import *

    Summary_df = pd.DataFrame()
    phone_spec = {}
    # 1.22 (when 8192 x 6144)
    # 2.44 (when 4096 x 3072)
    # 2.44 (crop 4096 x 2304)
    # 4.88 (when 2048 x 1152)
    # 4.88 (crop 1920 x 1080)
    Fill_phone_spec(phone_name="iPhone 14 Pro", pixel_size_um=1.22, diagonal_pixelN=10080, exif_fl_mm=24, converted_pixel_size_um=9.76)
    Fill_phone_spec(phone_name="Find X5 Pro", pixel_size_um=1.0, diagonal_pixelN=10240, exif_fl_mm=26.2, converted_pixel_size_um=4)
    Fill_phone_spec(phone_name="Galaxy S23 Ultra", pixel_size_um=0.6, diagonal_pixelN=20480, exif_fl_mm=23, converted_pixel_size_um=4.8)
    Fill_phone_spec(phone_name="Galaxy S22 Ultra", pixel_size_um=0.8, diagonal_pixelN=15000, exif_fl_mm=23, converted_pixel_size_um=2.4)
    Fill_phone_spec(phone_name="X50 Pro", pixel_size_um=0.8, diagonal_pixelN=10000, exif_fl_mm=25,
                    converted_pixel_size_um=1.6)
    # 0.8 (when 12000 x 9000)
    # 2.4 (when 4000 x 3000)
    # 2.4 (crop 4000 x 2250)
    # 2.4 (crop 3840 x 2160)
    # 4.8 (when 2000 x 1500)
    # 4.8 (crop 1920 x 1080)
    # # 1. 파일리스트 만들기
    folder = HK.select_folder_location(init_dir='D:\# Shared_Folder_HDD\# Image Database\# Functional Evaluation\# OIS\iPhone 14 Pro\EIS OFF\_Result')
    filelist = HK.make_filelist(folder, subdir=False, list_filetype=[".xlsx"])
    # # 2. 각각의 파일에 대해서

    for f in filelist:
        # f = HK.select_file(init_dir='D:\# Shared_Folder_HDD\# Image Database\# Functional Evaluation\# OIS\iPhone 14 Pro\EIS OFF\_Result')
        # 가진 조건 추출
        filename = os.path.splitext(f) # ('\\\\150.150.86.75\\# Shared_Folder_HDD\\# Image Database\\# Functional Evaluation\\# OIS\\# Video pool\\Galaxy S23 Ultra\\EIS ON\\_Result\\500-1200\\edit\\Galaxy S23 Ultra-W-x1.0-Default-ProVideo-Yaw-Pitch-0.5deg-1Hz','.xlsx')
        token = os.path.basename(filename[0]).split("_")
        phone_info = token[0].split("-")
        test_info = token[1].split("-")
        print(f"{phone_info=}")
        print(f"{test_info=}")
        # ['Galaxy S23 Ultra',
        #  'W',
        #  'x1.0',
        #  'Default',
        #  'ProVideo',
        #  'Yaw',
        #  'Pitch',
        #  '0.5deg',
        #  '1Hz']

        amp = test_info[-2]        #  '0.5deg',
        amp_for_cal = float(amp.replace("deg", ""))        # 0.5
        freq = test_info[-1] #  '1Hz'
        freq_for_cal = float(freq.replace("Hz", "")) #  1
        phone = phone_info[0]# ['Galaxy S23 Ultra',
        mode = test_info[0]
        vibration = test_info[1]
        excel_df = pd.read_excel(f)
        scale_factor = 1080 / excel_df.Image_Height.unique()[0]
        for roi in excel_df["ROI_No"].unique():
            df = excel_df[excel_df["ROI_No"] == roi]
            move = []
            frame_per_cycle = round(60 / freq_for_cal) # 1 cycle에 필요한 frame 수
            total_cycle = int(df.__len__() / frame_per_cycle)
            # patch_size = (df['Marker_Height'].mean() + df['Marker_Width'].mean()) / 2
            for c in range(total_cycle):
                tmp = df.iloc[0+c*frame_per_cycle:(c+1)*frame_per_cycle]
                ymin = tmp["Marker_Center_Y_full"].min()
                ymax = tmp["Marker_Center_Y_full"].max()
                xmin = tmp["Marker_Center_X_full"].min()
                xmax = tmp["Marker_Center_X_full"].max()
                measured_pixel_move = ((ymin - ymax) ** 2 + (xmin - xmax) ** 2) ** (1 / 2)  # 대각으로움직인 픽셀 측정
                move.append(measured_pixel_move)
            # amp_plus_minus = amp_for_cal / 2 # +-각도로 환산
            # theta_rad = (2 ** (1 / 2)) * (amp_plus_minus) * (pi / 180)
            # theta_rad = (대각 환산) * (+-각도) * (radian으로 환산)
            measured_pixel_move = np.average(move)
            # calculated_offset_move_mm_diagonal = 2 * phone_spec[phone]["fl"] * tan(theta_rad) # +-움직인각도로 환산 후 움직인 거리 계산 후 * 2
            # calculated_offset_pixel_move = calculated_offset_move_mm_diagonal / phone_spec[phone]["converted_pixel_size(um)"] *  1000
            # percentage = 100 * (1 - measured_pixel_move/calculated_offset_pixel_move)
            # SR = 20 * log(calculated_offset_pixel_move / measured_pixel_move, 10)

            tmp = pd.DataFrame.from_dict({"Phone" : [phone],
                                          "mode" : [mode],
                                          "vibration" : [vibration],
                                          "Amplitude(deg)" : [amp],
                                          "+-Angle" : [amp_for_cal / 2],
                                          "Frequency(Hz)" : [freq],
                                          "pixel size(um)" : phone_spec[phone]["pixel size(um)"],
                                          "diagonal pixel#": phone_spec[phone]["diagonal pixel#"],
                                          "sensor diagonal size(mm)": phone_spec[phone]["sensor diagonal size(mm)"],
                                          "crop factor": phone_spec[phone]["crop factor"],
                                          "35mm fl": phone_spec[phone]["35mm fl"],
                                          "real fl": phone_spec[phone]["fl"],
                                          # "caculated offset movement(mm)" : [calculated_offset_move_mm],
                                          # "caculated offset movement(mm)[diagonal]" : [calculated_offset_move_mm_diagonal],
                                          # "converted_pixel_size(um)": phone_spec[phone]["converted_pixel_size(um)"],
                                          # "Offpixel": [calculated_offset_pixel_move],
                                          "ROI" : [roi],
                                          "Pixel Movement" : [measured_pixel_move],
                                          "Scale factor" : [scale_factor],
                                          "Normalized Pixel Movement" : [measured_pixel_move * scale_factor],
                                          # "환산 움직임량(mm)" : [measured_pixel_move * phone_spec[phone]["converted_pixel_size(um)"] / 1000],
                                          # "보정률(백분율)" : [percentage],
                                          # "보정률(SR)" : [SR]
                                          })
            Summary_df = pd.concat([Summary_df, tmp], axis=0)
    Summary_df.to_excel(f"{folder}//{mode}_{phone}_Summary.xlsx")
    # print("hi")
    #
    #


    # # 시트로 저장
    # ## 2-1. 픽셀 떨림양 계산
    # ## 2-2. SR(db)계산
    #
    #
    #
    # ## 2-3. 백분율 계산