import os
import sys
import logging
import cv2
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

sys.path.append('../# HK')

from HK_func_file_folder_control import *
from HK_func_image_movie_file_control import *

def DetectionMark_test(f): # 현재는 input threshold값을 사용하지 않음
	dir = os.path.dirname(f)
	base = os.path.basename(f)
	f_token = os.path.splitext(base)
	name = f_token[0]
	ext = f_token[1]
	img_BGR = cv2.imread(f)
	img_BGR_for_all_contours = img_BGR.copy()
	img_BGR_for_rec_contours = img_BGR.copy()
	img_gray = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY) # CONVERT TO GRAY


	# Noise Filter 1 : 최대한 낮은 지점에서 thresholding > ui 살리기 위해
	threshold_value = np.percentile(img_gray.reshape(-1), 10) # 하위 10퍼센트 값
	ret, img_binary = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
	'''
	ret, dst = cv2.threshold(src, thresh, maxval, type)
	-. ret, thresh = 임계값
	-. img_binary = 출력 영상
	-. maxval = 임계값을 넘길시 적용할 value
	-. type = thresholding type 
	'''
	cv2.imwrite(f'{dir}//edited//{f_token[0]}-threshold{f_token[1]}', img_binary)
	#Contour를 찾아주는 함수
	contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # cv2.RETR_EXTERNAL = 가장 외곽의 컨투어만 찾음 , cv2.CHAIN_APPROX_NONE
	#1. 모든 컨투어 그리기
	cv2.drawContours(img_BGR_for_all_contours, contours, -1, (0,255,0), 3)

	#2. minAR을위한 새 리스트
	newcontours = []
	for idx, contour in enumerate(contours):

		rect = cv2.minAreaRect(contour) # 꼭 맞는 사각형 그리기
		box = cv2.boxPoints(rect) # box포인트로 변경
		box = np.int0(box) # contour로 변경
		cv2.drawContours(img_BGR_for_all_contours, [box], 0, (0, 0, 255), 3)
		# recarea = cv2.contourArea([box])


		(x,y), r = cv2.minEnclosingCircle(contour)
		center = (int(x), int(y))
		r = round(r)
		cv2.circle(img_BGR_for_all_contours, center, r, (255, 0, 0), 3)
		circlearea = r**2

		# print(recarea, circlearea)

		# newcontours.append()
		x_min = min([i[0][0] for i in contours[idx]])
		x_max = max([i[0][0] for i in contours[idx]])
		y_min = min([i[0][1] for i in contours[idx]])
		y_max = max([i[0][1] for i in contours[idx]])
		center_x = float((x_max + x_min) / 2)
		center_y = float((y_max + y_min) / 2)
		cv2.rectangle(img=img_BGR_for_all_contours, pt1=(x_min, y_min), pt2=(x_max, y_max), color=(0,255,0), thickness=1)
		cv2.line(img=img_BGR_for_all_contours, pt1=(round(center_x), round(y_min) - 5), pt2=(round(center_x), round(y_max + 5)), color=(0, 255, 0), thickness=1)
		cv2.line(img=img_BGR_for_all_contours, pt1=(round(x_min) - 5, round(center_y)), pt2=(round(x_max) + 5, round(center_y)), color=(0, 255, 0), thickness=1)
	cv2.imwrite(f'{dir}//edited//{f_token[0]}-allcontour{f_token[1]}', img_BGR_for_all_contours)


	# for cont in contours:
	#
	# for rect in newcontours:
	# 	box = cv2.boxPoints(rect)
	# 	box = np.int0(box)
	#
	# 	cv2.drawContours(img_BGR_for_all_contours, [box], 0, (0, 0, 255), 3)
	# cv2.imwrite(f'{dir}//{f_token[0]}-reccontour{f_token[1]}', img_BGR_for_all_contours)
		# approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
		# vtc = len(approx)
		# if vtc == 4:
		# 	newcontours.append(cont)

	# for idx in range(len(newcontours)):
	# 	x_min = min([i[0][0] for i in contours[idx]])
	# 	x_max = max([i[0][0] for i in contours[idx]])
	# 	y_min = min([i[0][1] for i in contours[idx]])
	# 	y_max = max([i[0][1] for i in contours[idx]])
	# 	center_x = float((x_max + x_min) / 2)
	# 	center_y = float((y_max + y_min) / 2)
	# 	cv2.rectangle(img=img_BGR_for_rec_contours, pt1=(x_min, y_min), pt2=(x_max, y_max), color=(0,255,0), thickness=1)
	# 	cv2.line(img=img_BGR_for_rec_contours, pt1=(round(center_x), round(y_min) - 5), pt2=(round(center_x), round(y_max + 5)), color=(0, 255, 0), thickness=1)
	# 	cv2.line(img=img_BGR_for_rec_contours, pt1=(round(x_min) - 5, round(center_y)), pt2=(round(x_max) + 5, round(center_y)), color=(0, 255, 0), thickness=1)
	# cv2.imwrite(f'{dir}//{f_token[0]}-reccontour{f_token[1]}', img_BGR_for_rec_contours)







	# filtered_by_rectangle_filter = []
	# width_n_noise_list = []
	# height_n_noise_list = []
	#
	# # Noise Filter 2 : 정사각 필터
	# for idx in range(len(contours)):
	# 	x_min = min([i[0][0] for i in contours[idx]])
	# 	x_max = max([i[0][0] for i in contours[idx]])
	# 	y_min = min([i[0][1] for i in contours[idx]])
	# 	y_max = max([i[0][1] for i in contours[idx]])
	#
	# 	width = x_max - x_min
	# 	height = y_max - y_min
	#
	# 	if height * 0.8 > width or width > height * 1.2: # 정사각 필터
	# 		continue
	# 	else:
	# 		# cv2.rectangle(img=img_roi, pt1=(x_min, y_min), pt2=(x_max, y_max), color=(0, 255, 0), thickness=1)
	# 		filtered_by_rectangle_filter.append(contours[idx])
	# 		width_n_noise_list.append(width)
	# 		height_n_noise_list.append(height)
	#
	#
	#
	# # 최대값 설정
	# width_n_noise_list.sort() # indexing을 위한 배열
	# height_n_noise_list.sort() # indexing을 위한 배열
	# hist = plt.hist(width_n_noise_list)
	# if hist[0][-1] < 9:
	# 	for i in range(int(hist[0][-1])):
	# 		width_n_noise_list.pop()
	# 		height_n_noise_list.pop()
	#
	# # Noise Filter 3 : 사이즈 필터 > 패치 절반 사이즈 이하의 노이즈 제거
	# width_median = (max(width_n_noise_list) + min(width_n_noise_list))/2
	# height_median = (max(height_n_noise_list) + min(height_n_noise_list))/2
	# width_list = [w for w in width_n_noise_list if w > width_median]
	# height_list = [h for h in height_n_noise_list if h > height_median]
	#
	# # Noise Filter 4 : 중앙값 기준 threshold >> 잘못 디텍팅한 큰 혹은 작은 녀석들 제거
	# threshold_width = np.median(width_list)
	# threshold_height = np.median(height_list)
	#
	# print(threshold_width, threshold_height)
	# dict_axis = {}
	# new_contours = []
	# for idx in range(len(filtered_by_rectangle_filter)):
	# 	x_min = min([i[0][0] for i in filtered_by_rectangle_filter[idx]])
	# 	x_max = max([i[0][0] for i in filtered_by_rectangle_filter[idx]])
	# 	y_min = min([i[0][1] for i in filtered_by_rectangle_filter[idx]])
	# 	y_max = max([i[0][1] for i in filtered_by_rectangle_filter[idx]])
	#
	# 	center_x = float((x_max + x_min) / 2)
	# 	center_y = float((y_max + y_min) / 2)
	#
	# 	width = x_max - x_min
	# 	height = y_max - y_min
	#
	# 	if (threshold_width * 0.8 < width < threshold_width * 1.2) and (threshold_height * 0.8 < height < threshold_height * 1.2 ): #
	# 		new_contours.append(filtered_by_rectangle_filter[idx])
	# 		dict_axis[idx] = {'x_max': x_max,
	# 						  'x_min': x_min,
	# 						  'y_max': y_max,
	# 						  'y_min': y_min,
	# 						  'center_x': center_x,
	# 						  'center_y': center_y}
	# 		logging.debug('Contour({}) >> Center (X, Y): ({}, {}), Max X: {}, Min X: {}, Max Y: {}, Min Y: {} '.format(idx, center_x, center_y, x_max, x_min, y_max, y_min))
	# 		cv2.rectangle(img=img, pt1=(x_min, y_min), pt2=(x_max, y_max), color=(0,255,0), thickness=1)
	# 		cv2.line(img=img, pt1=(round(center_x), round(y_min) - 5), pt2=(round(center_x), round(y_max + 5)), color=(0, 255, 0), thickness=1)
	# 		cv2.line(img=img, pt1=(round(x_min) - 5, round(center_y)), pt2=(round(x_max) + 5, round(center_y)), color=(0, 255, 0), thickness=1)
	#
	# # for cont in new_contours:
	# # 	approx = cv2.approxPolyDP(cont, cv2.arclength(cont, True) * 0.02, True)
	# # 	vtc = len(approx)
	# # 	print(vtc)
	#
	# if dict_axis.__len__() != 9:
	#
	# 	cv2.imwrite(filename=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png', img=img)
	#
	# # arrange 및 indexing
	# sorted_dict_axis = sorted(dict_axis.items(), key=lambda t: (t[1]['center_x'], t[1]['center_y']))
	# dict_axis = {}
	# roi = ["LT-1", "LB-1", "LT-2", "LB-2", "C", "RT-2", "RB-2", "RT-1", "RB-1"]
	# for idx, cont in enumerate(sorted_dict_axis):
	# 	dict_axis[roi[idx]] = sorted_dict_axis[idx][1]
	#
	# # cv2.imwrite(filename='03_CVT_to_contour.png', img=img)
	# # print() # for debugging
	# return img, dict_axis
	return 0,0

if __name__ == "__main__":
    f_list = make_filelist(target_dir = select_folder_location(init_dir = "D:\# Shared_Folder_HDD\# Python_Code_and_Tool\# OIS Analyzer GUI\SAMPLE\\framesample"), subdir=False, list_filetype=[".jpg"])
    for f in f_list:
        _,_ = DetectionMark_test(f)




