# -*- coding: utf-8 -*-
"""
# Author : HK, Lim
# e-mail : hklim@lginnotek.com
# Function List
	- select_file(init_dir='./', file_type=(("All files", "*.*"),))
	- select_folder_location(init_dir='./')
	- make_filelist(target_dir, subdir=False, list_filetype=None)
	- make_filelist_image(target_dir, subdir=False, list_filetype=None)
	- read_from_ini(file_name, section_name, item=None)
	- write_to_ini(file_name, section_name, dict_data)
"""

import os
import sys
import time
import datetime
import logging
from tqdm import tqdm
import exifread
import imghdr
import configparser
import tkinter
from tkinter import filedialog


def select_file(init_dir='./', file_type=(("All files", "*.*"),)):
    '''
    .. Note:: 1개의 파일 선택
    :return: filename (str) : 선택된 Filename (경로 포함)
    '''
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    filename = os.path.abspath(filedialog.askopenfilename(parent=tk_root,
                                                          initialdir=init_dir,
                                                          title='Please select a file',
                                                          filetypes=file_type))
    # print("Selected file: {}".format(filename))
    logging.info('Selected file: {}'.format(filename))
    return filename


def select_folder_location(init_dir='./'):
    '''
    .. Note:: Select folder location
    :param init_dir: Initial Directory (default = './')
    :return:
      selected_dir (str) : Selected folder location
    '''
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    selected_dir = os.path.abspath(filedialog.askdirectory(parent=tk_root,
                                                           initialdir=init_dir,
                                                           title='Please select a directory'))
    # print('Selected folder: {}'.format(select_dir))
    logging.info('Selected folder: {}'.format(selected_dir))
    return selected_dir


def make_filelist(target_dir, subdir=False, list_filetype=None):
	"""
    .. Note:: 선택된 폴더와 하위 폴더까지의 파일 리스트와 폴더 리스트를 Return 하는 함수
    :param target_dir: 리스트로 작성하고자 하는 root 폴더
    :param subdir: 하위 디렉토리 검색 여부 (Default : False)
    :param list_filetype: 리스트로 작성할 파일의 확장자 ex. ['.csv', '.json'] (Default : None)
    :return:
        file_list - 파일 리스트 (list) (경로명 포함)
    """
	_filelist_all = []
	file_list = []
	
	if subdir:
		for path, direct, files in os.walk(target_dir):
			# file_path = [os.path.join(path, file) for file in files]
			file_path = [os.path.abspath(os.path.join(path, file)) for file in files]
			# print(file_path)
			_filelist_all.extend(file_path)
	else:
		_filelist_all = [os.path.join(os.path.abspath(target_dir), file) for file in os.listdir(target_dir) if
		                 os.path.isfile(os.path.join(os.path.abspath(target_dir), file))]
	
	for _idx_file in tqdm(_filelist_all):
		if list_filetype != None:
			if os.path.splitext(_idx_file)[1].lower() in [idx.lower() for idx in list_filetype]:
				file_list.append(_idx_file)
		else:
			file_list.append(_idx_file)
	logging.info('Extension : {}, Total files: {}, Selected files: {}'.format(list_filetype, len(_filelist_all), len(file_list)))
	return file_list


def make_filelist_image(target_dir, subdir=False, list_filetype=None):
	"""
    .. Note:: 선택된 폴더와 하위 폴더까지의 파일 리스트와 폴더 리스트를 Return 하는 함수
    :param target_dir: 리스트로 작성하고자 하는 root 폴더
    :param subdir: 하위 디렉토리 검색 여부 (Default : False)
    :param list_filetype: 선택할 파일의 확장자 리스트 ex. ['.csv', '.json'] (Default : None)
    :return:
        file_list - 파일 리스트 (list) (경로명 포함)
    """
	_filelist_all = []
	file_list = []
	if subdir:
		for path, direct, files in os.walk(target_dir):
			# file_path = [os.path.join(path, file) for file in files]
			file_path = [os.path.abspath(os.path.join(path, file)) for file in files]
			# print(file_path)
			_filelist_all.extend(file_path)
	else:
		_filelist_all = [os.path.join(os.path.abspath(target_dir), file) for file in os.listdir(target_dir) if
		                 os.path.isfile(os.path.join(os.path.abspath(target_dir), file))]
	
	for _idx_file in tqdm(_filelist_all):
		if imghdr.what(file=_idx_file) != None:
			f = open(_idx_file, 'rb')  # Open image file for reading (binary mode)
			tags = exifread.process_file(f)  # Return Exif tags
			if len(tags) != 0:
				# print('{} : {}'.format(imghdr.what(file=_idx_file), _idx_file))
				# logging.debug('{} : {}'.format(imghdr.what(file=_idx_file), _idx_file))
				if list_filetype != None:
					if os.path.splitext(_idx_file)[1].lower() in [idx.lower() for idx in list_filetype]:
						file_list.append(_idx_file)
				else:
					file_list.append(_idx_file)
	logging.info('Total files: {}, Image files: {}'.format(len(_filelist_all), len(file_list)))
	return file_list


def read_from_ini(file_name, section_name, item=None):
	config = configparser.ConfigParser()
	# print('[{}] Logging Level: {}'.format(sys._getframe().f_code.co_name, logging.root.level))
	if os.path.exists(file_name):  # 파일이 존재할 경우
		# print('[{}] {} 파일이 존재합니다.'.format(sys._getframe().f_code.co_name, file_name))
		config.read(file_name)
		if section_name in config.sections():  # 섹션이 존재할 경우
			# print('[{}] {} 섹션이 존재합니다. {}'.format(sys._getframe().f_code.co_name, section_name, config[section_name]))
			logging.info('{} 섹션이 존재합니다. {}'.format(section_name, config[section_name]))
			if item == None:  # 전체 항목을 출력할 경우
				item_value = dict(config[section_name])
			else:
				try:  # 항목이 존재할 경우
					item_value = config[section_name][item]
					# print('[{}] file: {} -> [{}][{}] = {}'.format(sys._getframe().f_code.co_name, file_name, section_name, item, item_value))
					logging.debug('file: {} -> [{}][{}] = {}'.format(file_name, section_name, item, item_value))
				except:  # 항목이 존재하지 않을 경우
					item_value = ''
					# print('[{}] Section: {} > {} 항목을 찾을 수 없습니다.'.format(sys._getframe().f_code.co_name, section_name, item))
					logging.info('Section: {} > {} 항목을 찾을 수 없습니다.'.format(section_name, item))
		else:  # 섹션이 존재하지 않을 경우
			# print('[{}] {} 섹션이 존재하지 않습니다.'.format(sys._getframe().f_code.co_name, section_name))
			logging.info('{} 섹션이 존재하지 않습니다.'.format(section_name))
			item_value = ''
	else:
		# print('[{}] {} 파일이 존재하지 않습니다.'.format(sys._getframe().f_code.co_name, file_name))
		logging.info('{} 파일이 존재하지 않습니다.'.format(file_name))
		item_value = ''
	return item_value


def write_to_ini(file_name, section_name, dict_data):
	config = configparser.ConfigParser()
	# print('[{}] Logging Level: {}'.format(sys._getframe().f_code.co_name, logging.root.level))
	if os.path.exists(file_name):  # 파일이 존재할 경우
		# print('[{}] {} 파일이 존재합니다.'.format(sys._getframe().f_code.co_name, file_name))
		logging.info('{} 파일이 존재합니다.'.format(file_name))
		config.read(file_name)
		if section_name in config.sections():  # 섹션이 있을 경우
			# print('[{}] {} 섹션이 존재합니다.'.format(sys._getframe().f_code.co_name, section_name))
			logging.info('{} 섹션이 존재합니다.'.format(section_name))
			for idx in dict_data.keys():  # 섹션의 개별 항목 비교
				try:  # 섹션에 항목이 있는 경우
					# print('[{}] {} -> [{}][{}] = {}'.format(sys._getframe().f_code.co_name, file_name, section_name, idx, dict_data[idx]))
					logging.debug('file: {} -> [{}][{}] = {}'.format(file_name, section_name, idx, dict_data[idx]))
					if dict_data[idx] != config[section_name][idx]:  # 항목은 있는데 내용이 다를 경우 값 변경
						config[section_name][idx] = str(dict_data[idx])
					else:  # 항목이 있으며 값도 같은 경우
						pass
				except:  # 섹션에 항목이 없는 경우
					config[section_name][idx] = str(dict_data[idx])  # 항목 및 값 추가
		else:
			# print('[{}] {} 섹션이 존재하지 않습니다.'.format(sys._getframe().f_code.co_name, section_name))
			logging.info('{} 섹션이 존재하지 않습니다.'.format(section_name))
			config[section_name] = dict_data  # 항목 및 값 추가
	else:
		# print('[{}] {} 파일이 존재하지 않습니다.'.format(sys._getframe().f_code.co_name, file_name))
		logging.info('{} 파일이 존재하지 않습니다.'.format(file_name))
		config[section_name] = dict_data
	
	with open(file_name, 'w') as configfile:
		config.write(configfile)

def set_logging_level(logging_lv):
    # import datetime
    # print('[{}] Current Logging Level : ({}) {}'.format(sys._getframe().f_code.co_name, self.logging_level, _log_level_ini))
    if not os.path.exists('./_pylog'):
        os.makedirs('./_pylog')
    _now = datetime.datetime.now()
    _log_file = './_pylog/Log_PhoneControl_android_' + _now.strftime('%Y%m%d') + '.log'

    # 로그 생성 (console)
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging_lv)
    # log 출력 형식
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-7s] [%(filename)s (%(lineno)4d)] [%(funcName)20s] %(message)s')
    # log format 설정
    # logger.handlers[0].formatter = formatter

    # log를 파일에 출력
    file_handler = logging.FileHandler(_log_file, 'a', 'utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


if __name__ == "__main__":
	start_dir = r'C:\# Data\# Repository\Image_Quality_Tool\[Data] Input_Data'
	
	if 0:   # select_file Test
		filename = select_file(init_dir=start_dir, file_type=(("JPEG file", "*.jpg"), ("All files", "*.*"),))
		print('Selected File: {}'.format(filename))
	 
	if 0:   # select_folder_location Test
		folder_location = select_folder_location(init_dir=start_dir)
		print('Selected folder: {}'.format(folder_location))
	 
	if 0:   # make_filelist Test
		list_filetype = ['.png', '.bmp']
		file_list = make_filelist(target_dir=start_dir, subdir=True, list_filetype=None)
	
	if 0:   # make_filelist_image Test
		list_filetype = ['.png', '.bmp']
		file_list_image = make_filelist_image(target_dir=start_dir, subdir=True, list_filetype=None)
	 
	if 0:   # write_to_ini & read_from_ini Test
		set_file = 'setting_test.ini'
		if 1:
			write_default = {'Title': 'S/W Tool',
			                 'Version': '1.0.1',
			                 'Release': '2021-11-11',
			                 'Author': 'HK.Lim',
			                 'E-mail': 'hklim@lginnotek.com'}
			
			write_file = {'root_folder': 'C:\\# Data\\# Repository',
			              'save_folder': 'C:\\# Data\\# Repository',
			              'test_title': 150}
			write_file1 = {'test_title': 1110}
			
			write_to_ini(file_name=set_file, section_name='Default', dict_data=write_default)
			write_to_ini(file_name=set_file, section_name='File', dict_data=write_file)
			write_to_ini(file_name=set_file, section_name='Test', dict_data=write_default)
			# write_to_ini(file_name=set_file, section_name='File', dict_data=write_file1)
		else:
			read_value = read_from_ini(file_name=set_file, section_name='Default', item=None)
			print('result : {}'.format(read_value))
			read_value = read_from_ini(file_name=set_file, section_name='File', item='save_folder')
			print('result : {}'.format(read_value))

