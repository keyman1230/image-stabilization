import xml.etree.ElementTree as elemTree
import numpy as np
import math
import cv2
import os
import time
import csv
import pandas as pd

if __name__ == "__main__":
    try :
        tree = elemTree.parse('./input_data.xml') # parse file
        root = tree.getroot() # get root node

        pixel_x_pitch = float(root.find('pixel_x_pitch_mm').text) # 픽셀 pitch x ex) Galaxy S23 Ultra 0.0048mm
        pixel_y_pitch = float(root.find('pixel_y_pitch_mm').text) # 픽셀 pitch x ex) Galaxy S23 Ultra 0.0048mm
        oc_x = float(root.find('oc_x_pixel').text) # 주점의 x좌표, 편의상 이미지의 중심이라고 생각 ex)FHD기준 980
        oc_y = float(root.find('oc_y_pixel').text) # 주점의 y좌표, 편의상 이미지의 중심이라고 생각 ex)FHD기준 540
        EFL = float(root.find('EFL_mm').text) # 초점거리, ex) Galaxy S23 Ultra 6.5726511627907mm
        chart_distance = float(root.find("chart_distance_mm").text) # 차트와의 거리 ex) 1000mm
        XY_shake_angle = float(root.find('XY_shake_angle_degree').text) # 우리영상이 1deg 1hz > +-기준 0.707
        Roll_shake_angle = float(root.find('Roll_shake_angle_degree').text) # roll = 0
        XY_shakeaxis_angle = float(root.find('XY_shakeaxis_angle_degree').text) # ?
        csv_path = root.find('csv_path').text

        f = open(csv_path, 'r')
        rdr = csv.reader(f)
        num_world = sum(1 for row in rdr) - 1 # 행수  = 패치 수
        world_coordinate = np.full((4, num_world), 0.0) # 4행 5열 array 0.0
        intrinsic = np.full((3, 3), 0.0)

        f.seek(0)
        i = 0
        for line in rdr:
            if line[0].isnumeric():
                world_coordinate[0, i] = float(line[1])
                world_coordinate[1, i] = float(line[2])
                world_coordinate[2, i] = float(0.0)
                world_coordinate[3, i] = float(1.0)
                i = i + 1

        PFL_x = (chart_distance * EFL) / (chart_distance - EFL) / pixel_x_pitch
        PFL_y = (chart_distance * EFL) / (chart_distance - EFL) / pixel_y_pitch

        intrinsic[0, 0] = PFL_x
        intrinsic[0, 1] = 0
        intrinsic[0, 2] = oc_x
        intrinsic[1, 0] = 0
        intrinsic[1, 1] = PFL_y
        intrinsic[1, 2] = oc_y
        intrinsic[2, 0] = 0
        intrinsic[2, 1] = 0
        intrinsic[2, 2] = 1

        rodrigues_vector = np.full((3, 1), 0.0)
        rodrigues_vector_x = 1 * math.cos(XY_shakeaxis_angle * math.pi / 180.0)
        rodrigues_vector_y = 1 * math.sin(XY_shakeaxis_angle * math.pi / 180.0)
        rodrigues_vector_z = 0.0

        identity_mat = np.identity(3)

        rot_mat_roll = np.full((3, 3), 0.0)
        trans_mat_wc = np.full((3, 1), 0.0)
        trans_mat_wc[0, 0] = 0.0
        trans_mat_wc[1, 0] = 0.0
        trans_mat_wc[2, 0] = -chart_distance
        extrinsic_mat = np.full((3, 4), 0.0)
        v_pixel_mat = np.empty((0, 3, num_world), float)

        for i in range(0, 2):
            sign = 1
            if (i == 0):
                sign = 1
            else:
                sign = -1
            iter_yawpitch_angle = sign * XY_shake_angle * math.pi / 180.0
            iter_roll_angle = sign * Roll_shake_angle * math.pi / 180.0

            rot_mat_roll[0, 0] = math.cos(iter_roll_angle)
            rot_mat_roll[0, 1] = -math.sin(iter_roll_angle)
            rot_mat_roll[0, 2] = 0.0

            rot_mat_roll[1, 0] = math.sin(iter_roll_angle)
            rot_mat_roll[1, 1] = math.cos(iter_roll_angle)
            rot_mat_roll[1, 2] = 0.0

            rot_mat_roll[2, 0] = 0.0
            rot_mat_roll[2, 1] = 0.0
            rot_mat_roll[2, 2] = 1.0

            rodrigues_vector[0] = rodrigues_vector_x * iter_yawpitch_angle
            rodrigues_vector[1] = rodrigues_vector_y * iter_yawpitch_angle
            rodrigues_vector[2] = rodrigues_vector_z * iter_yawpitch_angle
            rot_mat_xy, _ = cv2.Rodrigues(rodrigues_vector)

            rot_mat_wc = rot_mat_xy.dot(rot_mat_roll)
            rot_mat_cw = np.linalg.inv(rot_mat_wc)
            trans_mat_cw = -np.linalg.inv(rot_mat_wc).dot(trans_mat_wc)

            extrinsic_mat[0:3, 0:3] = rot_mat_cw
            extrinsic_mat[0:3, 3:] = trans_mat_cw

            pixel_mat = intrinsic.dot(extrinsic_mat).dot(world_coordinate)
            pixel_mat[0] = pixel_mat[0] / pixel_mat[2]
            pixel_mat[1] = pixel_mat[1] / pixel_mat[2]
            pixel_mat[2] = pixel_mat[2] / pixel_mat[2]
            rows, cols = pixel_mat.shape
            pixel_mat = np.reshape(pixel_mat, (1, rows, cols))
            v_pixel_mat = np.append(v_pixel_mat, pixel_mat, axis=0)

        x_p2p = np.full(num_world, float)
        y_p2p = np.full(num_world, float)
        result_p2p = np.full((2, num_world * 2), 0, dtype=object)

        for i in range(num_world):
            x_p2p[i] = np.max(v_pixel_mat[:, 0, i]) - np.min(v_pixel_mat[:, 0, i])
            y_p2p[i] = np.max(v_pixel_mat[:, 1, i]) - np.min(v_pixel_mat[:, 1, i])
            result_p2p[0, 2 * i] = "p2p_x_{}".format(i)
            result_p2p[0, 2 * i + 1] = "p2p_y_{}".format(i)
            result_p2p[1, 2 * i] = x_p2p[i]
            result_p2p[1, 2 * i + 1] = y_p2p[i]
            print("i = {}, x_p2p = {}, y_p2p = {}".format(i, x_p2p[i], y_p2p[i]))

        millis = int(round(time.time() * 1000))
        save_result_directory = "./result"
        if not os.path.exists(save_result_directory):
            os.makedirs(save_result_directory)

        csv_file = "{}/result_{}.csv".format(save_result_directory, millis)
        dataframe = pd.DataFrame(result_p2p)
        dataframe.to_csv(csv_file, header=False, index=False)
    except Exception as e:
        print(e)
