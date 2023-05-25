# -*- coding: utf-8 -*-
"""
# Author : HK, Lim
# e-mail : hklim@lginnotek.com
# Function List
	- dng_converter_with_resize(file, res_width, res_height, use_camera_wb=True, img_format='.png', resize=False, cv2_inter=1)
	- raw_converter_with_resize(file, width, height, bpp, pix_order, res_width, res_height, img_format='.png', resize=False, cv2_inter=1)
	- exif_extraction_from_image(filelist)
"""

import os
import sys
sys.path.append("D:\# Shared_Folder_HDD\# Python_Code_and_Tool\# Jayce")
from image_processing import untitled
from calculation import cal
import datetime
import logging
import numpy as np
import pandas as pd
import cv2
import rawpy
import imghdr
from tqdm import tqdm
import exifread
from matplotlib import pyplot as plt

# Function - DNG Converter
def dng_converter_with_resize(file, res_width, res_height, use_camera_wb=True, img_format='.png', resize=False,
                              cv2_inter=1):
	'''
	.. Note:: DNG 파일을 PNG 파일로 변경하는 함수
	:param file: 경로가 포함된 DNG 파일 이름
	:param res_width: 저장할 이미지 width (resize)
	:param res_height: 저장할 이미지 height (resize)
	:param use_camera_wb: WhiteBalance 적용 여부 (Default : True)
	:param img_format: 저장할 이미지 format (Default : '.png')
	:param resize: 저장시 Resize 여부 (Default : False)
	:param cv2_inter: interpolation 방식 선택 ( 0 ~ 6 )
	:return:
		result : 변환 결과
		src : 이미지 데이터
	'''
	
	dict_cv2_inter = {0: 'INTER_NEAREST',
	                  1: 'INTER_LINEAR',
	                  2: 'INTER_CUBIC',
	                  3: 'INTER_AREA',
	                  4: 'INTER_LANCZOS4',
	                  5: 'INTER_LINEAR_EXACT',
	                  6: 'INTER_NEAREST_EXACT'
	                  }
	with rawpy.imread(file) as raw:
		src = raw.postprocess(use_camera_wb=use_camera_wb)
	if use_camera_wb:
		save_filename = os.path.splitext(file)[0] + '_convert_WB'
	else:
		save_filename = os.path.splitext(file)[0] + '_convert_NoWB'
	# resize
	if resize:
		save_filename = save_filename + '_resize_' + dict_cv2_inter[cv2_inter]
		src = cv2.resize(src, dsize=(res_width, res_height), interpolation=cv2_inter)
	if (img_format.lower() == '.jpg') or (img_format.lower() == '.jpeg'):
		result = cv2.imwrite(save_filename + img_format, cv2.cvtColor(src, cv2.COLOR_RGB2BGR),
		                     [int(cv2.IMWRITE_JPEG_QUALITY), 100])
	
	else:
		result = cv2.imwrite(save_filename + img_format, cv2.cvtColor(src, cv2.COLOR_RGB2BGR))
	# print('[{}] {} : ({}) {}'.format(sys._getframe().f_code.co_name, img_format, result, save_filename))
	logging.info('{} : ({}) {}'.format(img_format, result, save_filename))
	return result, src


# Function - RAW Converter
def raw_converter_with_resize(file, width, height, bpp, pix_order, res_width, res_height, ae_target, use_wb=False,
                              use_ae=False, img_format='.png', resize=False, cv2_inter=1):
	'''
	.. Note :: .raw 파일을 .png 파일로 변경하는 함수
	:param file: 경로가 포함된 raw 파일 이름
	:param width: .raw 파일의 이미지 width
	:param height: .raw 파일의 이미지 height
	:param bpp: bit per pixel
	:param pix_order: Pixel order
	:param res_width: 저장할 이미지 width (resize)
	:param res_height: 저장할 이미지 height (resize)
	:param ae_target: AE Target Value (0 ~ 255)
	:param use_wb: White Balance 사용 여부 (Default: False)
	:param use_ae: AE Target 사용 여부 (Default: False)
	:param img_format: 저장할 이미지 format (Default : '.png')
	:param resize: 저장시 Resize 여부 (Default : False)
	:param cv2_inter: interpolation 방식 선택 ( 0 ~ 6 )
	:return:
		result : 변환 결과
		src : 이미지 데이터
	'''
	print('[{}] Logging Level: {}'.format(sys._getframe().f_code.co_name, logging.root.level))
	dict_cv2_inter = {0: 'INTER_NEAREST',
	                  1: 'INTER_LINEAR',
	                  2: 'INTER_CUBIC',
	                  3: 'INTER_AREA',
	                  4: 'INTER_LANCZOS4',
	                  5: 'INTER_LINEAR_EXACT',
	                  6: 'INTER_NEAREST_EXACT'
	                  }
	blockSize = int(width * height * (bpp / 8))  # 파일 사이즈
	# 배열을 5바이트씩 나눈다.
	img = np.fromfile(file, np.uint8, blockSize, "").reshape((-1, 5))
	# 이중 마지막 5바이트(index 4) 열을 싹 다 삭제한다.
	img1 = np.delete(img, 4, axis=1)
	# 실제 이미지 크기로 다시 배열한다.
	conv = img1.reshape(height, width)
	# 변환!
	if pix_order == 'rggb':
		src = cv2.cvtColor(conv, cv2.COLOR_BayerRG2RGB)
	elif pix_order == 'grbg':
		src = cv2.cvtColor(conv, cv2.COLOR_BayerGR2RGB)
	elif pix_order == 'gbrg':
		src = cv2.cvtColor(conv, cv2.COLOR_BayerGB2RGB)
	elif pix_order == 'bggr':
		src = cv2.cvtColor(conv, cv2.COLOR_BayerBG2RGB)
	else:
		src = cv2.cvtColor(conv, cv2.COLOR_BayerRG2RGB)
	
	# Pre-ImageProcessing for WB & AE
	_b, _g, _r = cv2.split(src)
	logging.info('Average of R: {}, Average of G: {}, Average of B: {}'.format(_r.mean(), _g.mean(), _b.mean()))
	_factor_g_r = (_g / _r).mean()
	_factor_g_b = (_g / _b).mean()
	logging.info('G/R factor: {}, G/B factor: {}'.format(_factor_g_r, _factor_g_b))
	# White Balance Setting
	if use_wb:
		logging.info('White Balance is Enable.')
		_r = np.where((_r * _factor_g_r) > 255, 255, _r * _factor_g_r).astype('uint8')
		_b = np.where((_b * _factor_g_b) > 255, 255, _b * _factor_g_b).astype('uint8')
		src = cv2.merge((_b, _g, _r))
		save_filename = os.path.splitext(file)[0] + '_convert_WB'
	else:
		logging.info('White Balance is not checked.')
		save_filename = os.path.splitext(file)[0] + '_convert_NoWB'
	# Auto Exposure Target Setting
	if use_ae:
		logging.info('White Balance is Enable.')
		try:
			logging.info('Input AE Target: {}'.format(ae_target))
			_factor_g_target = ae_target / _g.mean()
			logging.info('AE factor (AE Target / G): {}'.format(_factor_g_target))
			_g = np.where((_g * _factor_g_target) > 255, 255, _g * _factor_g_target).astype('uint8')
			logging.info('Max value of G: {}, Min value of G: {}'.format(_g.max(), _g.min()))
			_factor_g_r = (_g / _r).mean()
			_factor_g_b = (_g / _b).mean()
			_r = np.where((_r * _factor_g_r) > 255, 255, _r * _factor_g_r).astype('uint8')
			_b = np.where((_b * _factor_g_b) > 255, 255, _b * _factor_g_b).astype('uint8')
			src = cv2.merge((_b, _g, _r))
			save_filename = save_filename + '_AE'
		except Exception as err:
			logging.error('AE Target Setting Error: (Target: {}) {}'.format(ae_target, err))
	else:
		logging.info('AE is not checked.')
		save_filename = save_filename + '_NoAE'
	# Resize Setting
	if resize:
		save_filename = save_filename + '_resize_' + dict_cv2_inter[cv2_inter]
		src = cv2.resize(src, dsize=(res_width, res_height), interpolation=cv2_inter)
	if (img_format.lower() == '.jpg') or (img_format.lower() == '.jpeg'):
		result = cv2.imwrite(save_filename + img_format, cv2.cvtColor(src, cv2.COLOR_RGB2BGR),
		                     [int(cv2.IMWRITE_JPEG_QUALITY), 100])
	else:
		result = cv2.imwrite(save_filename + img_format, cv2.cvtColor(src, cv2.COLOR_RGB2BGR))
	# print('[{}] {} : ({}) {}'.format(sys._getframe().f_code.co_name, img_format, result, save_filename))
	logging.info('{} : ({}) {}'.format(img_format, result, save_filename))
	return result, src


# Function - EXIF Data Extraction
def exif_extraction_from_image(filelist):
	'''
	.. Note:: 이미지 파일의 EXIF 정보(DataFrame)를 Return하는 함수
	:param filelist: Image File List (list)
	:return: exif_infomation (DataFrame)
	'''
	df_exif_information = pd.DataFrame()
	
	for idx in tqdm(filelist):
		if imghdr.what(file=idx) != None:
			f = open(idx, 'rb')  # Open image file for reading (binary mode)
			tags = exifread.process_file(f)  # Return Exif tags
			if len(tags) != 0:
				logging.debug('{} : {}'.format(imghdr.what(file=idx), os.path.basename(idx)))
				tags['filename'] = os.path.basename(idx)
				tags['dirname'] = os.path.dirname(idx)
				df_exif_information = pd.concat([df_exif_information, pd.DataFrame.from_dict(tags, orient='index').T],
				                                axis=0, join='outer')
			else:
				# print(os.path.splitext(idx)[1].lower(), ' : ', len(tags))
				logging.debug('Exif Data is empty. : {}'.format(os.path.basename(idx)))
				pass
		else:
			# print('{} : {}'.format(imghdr.what(file=idx), os.path.basename(idx)))
			logging.debug('This file is not image file. : {}'.format(os.path.basename(idx)))
			pass
	return df_exif_information


def get_info_from_movie_file(filename):
	vidcap = cv2.VideoCapture(filename)
	dict_info = {'Width': int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
	             'Height': int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
	             'nFrame': int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1,
	             'FPS': vidcap.get(cv2.CAP_PROP_FPS)}
	logging.info('Video File Information: {}'.format(dict_info))
	return dict_info

def extraction_frame(filename, frame_no):
	vidcap = cv2.VideoCapture(filename)
	vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_no) # 속성값 수정 명령어
	ret, frame = vidcap.read()
	if ret:
		# logging.info('Frame Information >> Frame No.: {}, Frame Time: {}, Frame Width : {}, Frame Height : {}'.format(frame_no, vidcap.get(cv2.CAP_PROP_POS_MSEC), vidcap.get(cv2.CAP_PROP_FRAME_WIDTH), vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
		return frame, vidcap.get(cv2.CAP_PROP_POS_MSEC), vidcap.get(cv2.CAP_PROP_FRAME_WIDTH), vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	else:
		# logging.info(f'Frame Information >> Frame No.: {frame_no},Frame Read Fail !!!')
		return None, None, None, None

# def cal_width_height(contour):
# 	x_min = min([i[0][0] for i in contour])
# 	x_max = max([i[0][0] for i in contour])
# 	y_min = min([i[0][1] for i in contour])
# 	y_max = max([i[0][1] for i in contour])
# 	width = x_max - x_min
# 	height = y_max - y_min
# 	center_x = float((x_max + x_min) / 2)
# 	center_y = float((y_max + y_min) / 2)
# 	return width, height, center_x, center_y

# def cal_distance(x1, x2, y1, y2):
# 	return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)
def fitting_rectangle(contour):
	rect = cv2.minAreaRect(contour)  # 꼭 맞는 사각형 그리기
	box = cv2.boxPoints(rect)  # box포인트로 변경
	p1, p2, p3, p4 = box
	l1 = cal_distance(p1[0], p2[0], p1[1], p2[1])
	l2 = cal_distance(p2[0], p3[0], p2[1], p3[1])
	return l1, l2

def is_square(contour, threshold_error=0.2):
	contour_area = cv2.contourArea(contour)  # contour의 넓이
	l1, l2 = fitting_rectangle(contour)
	square_area = l1 * l2 # fitting rectangle의 넓이
	if l1 * (1-threshold_error) < l2 < l1 * (1+threshold_error):# 각 변의 길이 비율 비교
		if square_area * (1-threshold_error) < contour_area < square_area * (1+threshold_error): # 넓이 비교
			return True

	return False

def is_rect(contour):
	l1, l2 = fitting_rectangle(contour)
	recarea = l1 * l2
	# box = np.int0(box)  # contour로 변경
	# cv2.drawContours(img_BGR_for_all_contours, [box], 0, (0, 0, 255), 3)
	# recarea = cv2.contourArea([box])

	(x, y), r = cv2.minEnclosingCircle(contour)
	# center = (int(x), int(y))
	# r = round(r)
	# cv2.circle(img_BGR_for_all_contours, center, r, (255, 0, 0), 3)
	circlearea = r ** 2 * np.pi
	if circlearea > recarea:
		return True
	else:
		return False

def DetectionMark(file, frame_no, img, save): # 현재는 input threshold값을 사용하지 않음
	'''

	:param file:
	:param frame_no:
	:param img:
	:return:
	'''
	dir = os.path.dirname(file) # 파일이 저장된 폴더 위치
	base = os.path.basename(file) # 파일의 basename. ex) sample.mp4
	f_token = os.path.splitext(base) # 확장자 분리 ex) sample, .mp4
	name = f_token[0] # 확장자 제외 이름 ex) sample
	ext = f_token[1] # 확장자 ex) .mp4

	img_BGR_for_all_contours = img.copy() # 모든 컨투어를 그리기 위한 이미지 복사
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT TO GRAY
	if save:
		cv2.imwrite(f'{dir}//{name}-Frame{frame_no}-Gray.jpg', img_gray)

	# Filter1 : Thresholding >> 최대한 낮은 지점에서 thresholding > ui에 가려진 패치를 살리기 위해
	threshold_value = np.percentile(img_gray.reshape(-1), 10) # 하위 10퍼센트 값
	ret, img_binary = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
	'''
	ret, dst = cv2.threshold(src, thresh, maxval, type)
	-. ret, thresh = 임계값
	-. img_roi_binary = 출력 영상
	-. maxval = 임계값을 넘길시 적용할 value
	-. type = thresholding type 
	'''
	if save:
		cv2.imwrite(f'{dir}//{name}-Frame{frame_no}-Binary.jpg', img_binary)

	#Contour를 찾아주는 함수 ( pass )
	contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # cv2.RETR_EXTERNAL = 가장 외곽의 컨투어만 찾음 , cv2.CHAIN_APPROX_NONE

	if save:
		cv2.drawContours(img_BGR_for_all_contours, contours, -1, (0, 255, 0), 3)
		cv2.imwrite(f'{dir}//{name}-Frame{frame_no}-All contours.jpg', img_BGR_for_all_contours)

	square_filtered = []
	width_n_noise_list = []
	height_n_noise_list = []

	# Filter2 : 정사각 필터 >> 직사각형, 괴상한 오목다각형 제거 가능, 원과 사각형 분리 가능
	for contour in contours:
		if is_square(contour) and is_rect(contour):

			square_filtered.append(contour)
			width, height, _, _ = cal_width_height(contour)
			width_n_noise_list.append(width)
			height_n_noise_list.append(height)


	if save:
		cv2.drawContours(img_BGR_for_all_contours, square_filtered, -1, (0, 0, 255), 3)
		cv2.imwrite(f"{dir}//{name}-Frame{frame_no}-filter2 contours.jpg", img_BGR_for_all_contours)

	# Filter3 : 사이즈 필터 >> 작은 사이즈의 노이즈들 제거

	threshold_width = max(width_n_noise_list)/2
	threshold_height = max(height_n_noise_list)/2

	# print(threshold_width, threshold_height)
	dict_axis = {}
	new_contours = []
	for idx in range(len(square_filtered)):
		x_min = min([i[0][0] for i in square_filtered[idx]])
		x_max = max([i[0][0] for i in square_filtered[idx]])
		y_min = min([i[0][1] for i in square_filtered[idx]])
		y_max = max([i[0][1] for i in square_filtered[idx]])

		center_x = float((x_max + x_min) / 2)
		center_y = float((y_max + y_min) / 2)

		width = x_max - x_min
		height = y_max - y_min
		if width > threshold_width and height > threshold_height:
		# if (threshold_width * 0.8 < width < threshold_width * 1.2) and (threshold_height * 0.8 < height < threshold_height * 1.2 ): #
			new_contours.append(square_filtered[idx])
			dict_axis[idx] = {'x_max': x_max,
							  'x_min': x_min,
							  'y_max': y_max,
							  'y_min': y_min,
							  'center_x': center_x,
							  'center_y': center_y}
			logging.debug('Contour({}) >> Center (X, Y): ({}, {}), Max X: {}, Min X: {}, Max Y: {}, Min Y: {} '.format(idx, center_x, center_y, x_max, x_min, y_max, y_min))
			cv2.rectangle(img=img, pt1=(x_min, y_min), pt2=(x_max, y_max), color=(0,255,0), thickness=1)
			cv2.line(img=img, pt1=(round(center_x), round(y_min) - 5), pt2=(round(center_x), round(y_max + 5)), color=(0, 255, 0), thickness=1)
			cv2.line(img=img, pt1=(round(x_min) - 5, round(center_y)), pt2=(round(x_max) + 5, round(center_y)), color=(0, 255, 0), thickness=1)

	if save:
		cv2.drawContours(img_BGR_for_all_contours, new_contours, -1, (255, 0, 0), 3)
		cv2.imwrite(f"{dir}//{name}-Frame{frame_no}-filter3 contours.jpg", img_BGR_for_all_contours)
		if len(new_contours) != 9:
			print(f"{dir}//{name}-Frame{frame_no}-filter3 contours.jpg >> contour : {len(new_contours)}")

	# # # arrange 및 indexing
	# LT, LB, RT, RB = {},{},{},{}
	# w, h, _ = img.shape
	# img_center_y, img_center_x = h/2, w/2
	# for idx, key in enumerate(dict_axis.keys()):
	# 	x, y = dict_axis[key]["center_x"], dict_axis[key]["center_y"]
	# 	d = cal_distance(x, img_center_x, y, img_center_y)
	# 	if not idx:
	# 		refer = d
	# 		center_key = key
	# 	else:
	# 		if d < refer:
	# 			refer = d
	# 			center_key = key
	# center = dict_axis[center_key]
	# center_x, center_y = center["center_x"], center["center_y"]
	#
	# for key, items in dict_axis.items():
	# 	x, y = items["center_x"], items["center_y"]
	# 	items["distance_from_center"] = cal_distance(x, center_x, y, center_y)
	# 	if x < center_x and y < center_y:
	# 		LT[key] = items
	# 	elif x < center_x and y > center_y:ㄹㄹ
	# 		LB[key] = items
	# 	elif x > center_x and y < center_y:
	# 		RT[key] = items
	# 	elif x > center_x and y > center_y:
	# 		RB[key] = items
	# 	else:
	# 		pass
	# del dict_axis
	# dict_axis = {}
	# sorted_LT = sorted(LT.items(), key=lambda t: t[1]["distance_from_center"])
	# sorted_LB = sorted(LB.items(), key=lambda t: t[1]["distance_from_center"])
	# sorted_RT = sorted(RT.items(), key=lambda t: t[1]["distance_from_center"])
	# sorted_RB = sorted(RB.items(), key=lambda t: t[1]["distance_from_center"])
	#
	# for idx, items in enumerate(sorted_LT):
	# 	dict_axis[f"LT-{idx}"] = items[1]
	# for idx, items in enumerate(sorted_RT):
	# 	dict_axis[f"RT-{idx}"] = items[1]
	# for idx, items in enumerate(sorted_LB):
	# 	dict_axis[f"LB-{idx}"] = items[1]
	# for idx, items in enumerate(sorted_RB):
	# 	dict_axis[f"RB-{idx}"] = items[1]


	return img, dict_axis



if __name__ == "__main__":
	import os
	import sys
	import cv2
	from HK_func_file_folder_control import make_filelist
	import matplotlib.pyplot as plt
	
	# logging.basicConfig(level=logging.INFO)
	# filename = select_file_v1(init_dir='./')
	# filename = r'C:\# Data\# Repository\# Github\01_Image_Quality\[Data] Input_Data\[DNG] Zoom Test\SFRplus_LD65_6500_2000_6500_2000_Pixel6P_x4.0_PXL_20211220_074513960.dng'
	
	if 0:
		filepath = r'C:\# Data\# Repository\# Github\01_Image_Quality\[Data] Input_Data'
		os.chdir(filepath)
		filelist = make_filelist(target_dir=filepath, subdir=True, list_filetype=['.raw'])
		for idx_file in filelist:
			print('filename: {}'.format(idx_file))
			for idx_inter in range(7):
				result, src = raw_converter_with_resize(file=os.path.relpath(idx_file), width=4032, height=3024,
				                                        bpp=10, pix_order='gbrg', res_width=2016, res_height=1512,
				                                        img_format='.png', resize=True, cv2_inter=idx_inter)
				print('Result: {}'.format(result))
	
	if 0:
		filepath = r'C:\# Data\# Repository\# Github\01_Image_Quality\[Data] Input_Data\[raw] grabber_image'
		os.chdir(filepath)
		filelist = make_filelist(target_dir=filepath, subdir=True, list_filetype=['.raw'])
		for idx_file in filelist:
			print('filename: {}'.format(idx_file))
			for idx_inter in range(7):
				result, src = raw_converter_with_resize(file=os.path.relpath(idx_file), width=4032, height=3024,
				                                        bpp=10, pix_order='grbg', res_width=2016, res_height=1512,
				                                        img_format='.png', resize=True, cv2_inter=idx_inter)
				print('Result: {}'.format(result))
	
	if 0:
		# filepath = r'C:\# Data\# Repository\# Github\01_Image_Quality\[Data] Input_Data\[Image] DNG_to_PNG'
		filepath = r'C:\# Data\# Repository\Image_Quality_Tool\[Data] Input_Data\[DNG] Zoom Test'
		# os.chdir(filepath)
		filelist = make_filelist(target_dir=filepath, subdir=True, list_filetype=['.dng'])
		for idx_file in filelist:
			print('filename: {}'.format(idx_file))
			# for idx_inter in range(7):
			idx_inter = 2
			result, src = dng_converter_with_resize(file=os.path.relpath(idx_file), res_width=4080, res_height=3072,
			                                        use_camera_wb=True, img_format='.png', resize=False,
			                                        cv2_inter=idx_inter)
			print('Result: {}'.format(result))
	
	if 1:
		filepath = r'C:\# Data\# Repository\Image_Analysis_Tool\[Data] Test Data\[Image] DNG Image File'
		filelist = make_filelist(target_dir=filepath, subdir=True, list_filetype=['.dng'])
		df_exif_data = exif_extraction_from_image(filelist=filelist)
