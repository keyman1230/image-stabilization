# -*- coding: utf-8 -*-
"""
Created on 2021-12-09 (Thu)
@author: HK, Lim
"""

# Import
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

def set_logging_level(logging_lv):
    import datetime
    if not os.path.isdir('./_pylog'):
        os.mkdir('./_pylog')
    _now = datetime.datetime.now()
    _log_file = './_pylog/Log_OIS_Analyzer_' + _now.strftime('%Y%m%d') + '.log'

    # 로그 생성 (console)
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging_lv)
    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - [%(levelname)-6s] [%(filename)s (%(lineno)-3d)] [%(funcName)-8s] %(message)s')
    # log format 설정
    logger.handlers[0].formatter = formatter

    # log를 파일에 출력
    file_handler = logging.FileHandler(_log_file, 'a', 'utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

form_class = uic.loadUiType("GUI_OIS_Analyzer.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.list_selected_idx_filelist_search = []
        self.list_selected_idx_filelist_select = []
        self.list_filelist_search = []
        self.list_filelist_select = []
        self.list_roi_select = []
        self.info_default = {'Title': 'OIS Analyzer',
                             'Version': '1.1',
                             'Release': '2022-06-09',
                             'Author': 'HK, Lim',
                             'E-mail': 'hklim@lginnotek.com',
                             'Company': 'LG Innotek Co., Ltd.'}
        self.setWindowTitle(self.info_default['Title'] + ' v' + self.info_default['Version'] + ' - ' + self.info_default['Company'])
        self.set_file = 'Env_' + self.info_default['Title'].replace(' ', '_') + '.ini'
        write_to_ini(file_name=self.set_file, section_name='Default', dict_data=self.info_default)
        # ini에 저장된 기존 사용 Option 불러오기 - Logging Level
        _level_list = {'NOTSET': logging.NOTSET,        # 0
                       'DEBUG': logging.DEBUG,          # 10
                       'INFO': logging.INFO,            # 20
                       'WARNING': logging.WARNING,      # 30
                       'ERROR': logging.ERROR,          # 40
                       'CRITICAL': logging.CRITICAL}    # 50
        _log_level_ini = read_from_ini(file_name=self.set_file, section_name='Log', item='logging level')
        if _log_level_ini.upper() in _level_list.keys():
            _logging_level = _level_list.get(_log_level_ini)
            self.comboBox_debug_level.setCurrentText(_log_level_ini)
        else:
            _logging_level = _level_list.get('WARNING')
            self.comboBox_debug_level.setCurrentText('WARNING')
            write_to_ini(file_name=self.set_file, section_name='Log', dict_data={'logging level': 'WARNING'})
       
        # Logging Level 설정
        set_logging_level(logging_lv=_logging_level)
        logging.warning('Current Logging Level : {}'.format(logging.root.level))
       
        # ini에 저장된 기존 사용 Option 불러오기 - last folder
        self.folder_location = read_from_ini(file_name=self.set_file, section_name='History', item='last folder')
        self.lineEdit_path.setText(os.path.abspath(self.folder_location))

    def menu_about(self):
        # App 정보 창 설정
        QMessageBox.about(self, 'About', "<h2>" + self.info_default['Title'] + "</h2>"
                                         "v" + self.info_default['Version'] + " ( " + self.info_default['Release'] + " )<hr>"
                                         "Create by " + self.info_default['Author'] + "<br>"
                                         "e-mail " + self.info_default['E-mail'] + "<br>"
                                         "Company : " + self.info_default['Company'] + "<br>"
                                         "Copyrightⓒ" + self.info_default['Release'][0:4] + " " + self.info_default['Author'] + " All rights reserved." + "<hr>"
                          )

    def select_crop_roi_rect(self):
        _label_width = self.label_view_image.width()
        _label_height = self.label_view_image.height()
        _roi_x = [int((self.selected_file_info_movie_in_search['Width'] / _label_width) * self.mousePress_x), int((self.selected_file_info_movie_in_search['Width'] / _label_width) * self.mouseRelease_x)]
        _roi_y = [int((self.selected_file_info_movie_in_search['Height'] / _label_height) * self.mousePress_y), int((self.selected_file_info_movie_in_search['Height'] / _label_height) * self.mouseRelease_y)]
        self.lineEdit_roi_start_x.setText(str(min(_roi_x)))
        self.lineEdit_roi_start_y.setText(str(min(_roi_y)))
        self.lineEdit_roi_end_x.setText(str(max(_roi_x)))
        self.lineEdit_roi_end_y.setText(str(max(_roi_y)))
        self.lineEdit_roi_width.setText(str(max(_roi_x) - min(_roi_x)))
        self.lineEdit_roi_height.setText(str(max(_roi_y) - min(_roi_y)))
        self.draw_image_from_ndarrary()
        self.statusBar().showMessage('Selected ROI - Start: ({}, {}),  End: ({}, {}),  Size: ({} x {})'.format(min(_roi_x), min(_roi_y), max(_roi_x), max(_roi_y), max(_roi_x) - min(_roi_x), max(_roi_y) - min(_roi_y)))
        logging.info('Selected ROI - Start: ({}, {}),  End: ({}, {}),  Size: ({} x {})'.format(min(_roi_x), min(_roi_y), max(_roi_x), max(_roi_y), max(_roi_x) - min(_roi_x), max(_roi_y) - min(_roi_y)))

    def getPos_mousePress(self, event):
        _x = event.pos().x()
        _y = event.pos().y()
        if _x < 0:
            self.mousePress_x = 0
        elif _x > self.label_view_image.width():
            self.mousePress_x = self.label_view_image.width()
        else:
            self.mousePress_x = _x
        if _y < 0:
            self.mousePress_y = 0
        elif _y > self.label_view_image.height():
            self.mousePress_y = self.label_view_image.height()
        else:
            self.mousePress_y = _y
        # _convert_width = int((self.selected_file_info_movie_in_search['Width'] / self.label_view_image.width()) * self.mousePress_x)
        # _convert_height = int((self.selected_file_info_movie_in_search['Height'] / self.label_view_image.height()) * self.mousePress_y)
        # print('[{}] Mouse Pressed: ({}, {})'.format(sys._getframe().f_code.co_name, _convert_width, _convert_height))

    def getPos_mouseMove(self, event):
        _x = event.pos().x()
        _y = event.pos().y()
        if _x < 0:
            self.mouseMove_x = 0
        elif _x > self.label_view_image.width():
            self.mouseMove_x = self.label_view_image.width()
        else:
            self.mouseMove_x = _x
        if _y < 0:
            self.mouseMove_y = 0
        elif _y > self.label_view_image.height():
            self.mouseMove_y = self.label_view_image.height()
        else:
            self.mouseMove_y = _y
        _press_x = int((self.selected_file_info_movie_in_search['Width'] / self.label_view_image.width()) * self.mousePress_x)
        _press_y = int((self.selected_file_info_movie_in_search['Height'] / self.label_view_image.height()) * self.mousePress_y)
        _current_x = int((self.selected_file_info_movie_in_search['Width'] / self.label_view_image.width()) * self.mouseMove_x)
        _current_y = int((self.selected_file_info_movie_in_search['Height'] / self.label_view_image.height()) * self.mouseMove_y)
        # print('[{}] Mouse Move: ({}, {})'.format(sys._getframe().f_code.co_name, _convert_width, _convert_height))
        self.statusBar().showMessage('Press: ({}, {}),  Cur Position: ({}, {}),  WxH: ({} x {})'.format(_press_x, _press_y, _current_x, _current_y, abs(_press_x - _current_x), abs(_press_y - _current_y)))

    def getPos_mouseRelease(self, event):
        _x = event.pos().x()
        _y = event.pos().y()
        if _x < 0:
            self.mouseRelease_x = 0
        elif _x > self.label_view_image.width():
            self.mouseRelease_x = self.label_view_image.width()
        else:
            self.mouseRelease_x = _x
        if _y < 0:
            self.mouseRelease_y = 0
        elif _y > self.label_view_image.height():
            self.mouseRelease_y = self.label_view_image.height()
        else:
            self.mouseRelease_y = _y
        # _convert_width = int((self.selected_file_info_movie_in_search['Width'] / self.label_view_image.width()) * self.mouseRelease_x)
        # _convert_height = int((self.selected_file_info_movie_in_search['Height'] / self.label_view_image.height()) * self.mouseRelease_y)
        # logging.debug('Mouse Released >> ({}, {})'.format(convert_width, _convert_height))
        self.select_crop_roi_rect()

    def draw_image_from_file(self, filename):
        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        _qPixmapFileVar = QPixmap()
        _qPixmapFileVar.load(filename)
        logging.info('qPixmapFileVar (w x h) : {} x {}'.format(_qPixmapFileVar.width(), _qPixmapFileVar.height()))
        _qPixmapFileVar = _qPixmapFileVar.scaledToHeight(self.label_view_image.height())
        self.label_view_image.setPixmap(_qPixmapFileVar)

    def draw_image_from_ndarrary(self):
        # self.label_view_image.clear()
        self.label_view_image.mousePressEvent = self.getPos_mousePress
        self.label_view_image.mouseReleaseEvent = self.getPos_mouseRelease
        self.label_view_image.mouseMoveEvent = self.getPos_mouseMove
        _frame = self.extracted_frame.copy()
        if (self.lineEdit_roi_width.text() != '0') and (self.lineEdit_roi_height.text() != '0'):
            _frame = cv2.rectangle(_frame, (int(self.lineEdit_roi_start_x.text()), int(self.lineEdit_roi_start_y.text())), (int(self.lineEdit_roi_end_x.text()), int(self.lineEdit_roi_end_y.text())), (255, 255, 0), 20, cv2.LINE_8)
        # else:
        #     _frame = _frame.copy()
        # QPixmap 객체 생성 후 ndarrary를 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        _height, _width, _channel = _frame.shape
        _bytesPerLine = 3 * _width
        _qImg = QImage(_frame, _width, _height, _bytesPerLine, QImage.Format_RGB888).rgbSwapped()   # RGB -> BGR 순서 변경
        # _qImg = QImage(_frame, _width, _height, _bytesPerLine, QImage.Format_RGB888)
        _qPixmapFileVar = QPixmap.fromImage(_qImg)
        logging.info('qPixmapFileVar (w x h) : {} x {}'.format(_qPixmapFileVar.width(), _qPixmapFileVar.height()))
        _qPixmapFileVar = _qPixmapFileVar.scaledToHeight(self.label_view_image.height())
        self.label_view_image.setPixmap(_qPixmapFileVar)

    def update_lineedit_path(self):
        # 검색하고자 하는 폴더 경로를 lineEdit에 업데이트
        self.lineEdit_path.setText(os.path.abspath(self.folder_location))

    def update_lineedit_path_manual(self):
        self.folder_location = self.lineEdit_path.text()
        logging.warning('Change folder location to {}'.format(self.folder_location))

    def update_frame_no(self):   # 수정중
        _value = self.horizontalSlider_frame_no.value()
        self.extracted_frame, _runtime, frame_width, frame_height  = extraction_frame(filename=self.selected_file_in_search, frame_no=_value-1)
        logging.info('Slider value: {} >>> width: {} >>> Height: {}'.format(_value, self.extracted_frame.shape[1], self.extracted_frame.shape[0]))
        self.lineEdit_frame_no.setText(str(_value))
        self.lineEdit_width.setText(str(self.extracted_frame.shape[1]))
        self.lineEdit_height.setText(str(self.extracted_frame.shape[0]))
        self.lineEdit_fps.setText(str(round(self.selected_file_info_movie_in_search['FPS'], 1)))
        # self.draw_image_from_ndarrary(frame=_extracted_frame)
        self.draw_image_from_ndarrary()

    def clear_search_list(self):
        self.tableWidget_filelist_search.clear()
        self.tableWidget_filelist_search.setColumnCount(3)
        self.tableWidget_filelist_search.setHorizontalHeaderLabels(['Filename', 'Type', 'Path'])
        self.tableWidget_filelist_search.horizontalHeaderItem(0).setToolTip('파일명...')
        self.tableWidget_filelist_search.horizontalHeaderItem(1).setToolTip('파일 형식...')
        self.tableWidget_filelist_search.horizontalHeaderItem(2).setToolTip('경로...')
        self.tableWidget_filelist_search.setColumnWidth(0, 300)
        # self.tableWidget_filelist_search.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_filelist_search.setRowCount(0)
        self.list_filelist_select.clear()

    def clear_select_list(self):
        self.tableWidget_filelist_select.clear()
        self.tableWidget_filelist_select.setColumnCount(3)
        self.tableWidget_filelist_select.setHorizontalHeaderLabels(['Filename', 'Type', 'Path'])
        self.tableWidget_filelist_select.horizontalHeaderItem(0).setToolTip('파일명...')
        self.tableWidget_filelist_select.horizontalHeaderItem(1).setToolTip('파일 형식...')
        self.tableWidget_filelist_select.horizontalHeaderItem(2).setToolTip('경로...')
        self.tableWidget_filelist_select.setColumnWidth(0, 300)
        # self.tableWidget_filelist_select.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget_filelist_select.setRowCount(0)
        self.list_filelist_select.clear()

    def clear_frame_view(self):
        self.label_view_image.clear()
        self.lineEdit_roi_start_x.setText(str(0))
        self.lineEdit_roi_start_y.setText(str(0))
        self.lineEdit_roi_end_x.setText(str(0))
        self.lineEdit_roi_end_y.setText(str(0))
        self.lineEdit_roi_width.setText(str(0))
        self.lineEdit_roi_height.setText(str(0))

    def click_btn_open(self):
        self.statusBar().showMessage('Selecting Folder . . .')
        # -+-+-+-+-+-+-+-+-+- [...] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- #
        if self.folder_location != '':
            self.folder_location = select_folder_location(init_dir=self.folder_location)
        else:
            self.folder_location = select_folder_location(init_dir='./')
        logging.warning('Selected Folder : {}'.format(self.folder_location))
        self.update_lineedit_path()
        self.clear_select_list()
        # -+-+-+-+-+-+-+-+-+- [...] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- #
        self.statusBar().showMessage('Selecting Complete.')

    #### Search Option
    def check_search_option(self):
        # file type Option check
        self.list_filetype = []
        if self.checkBox_mp4.isChecked():
            self.list_filetype.append('.mp4')
        if self.checkBox_avi.isChecked():
            self.list_filetype.append('.avi')
        if self.checkBox_mov.isChecked():
            self.list_filetype.append('.mov')
        if self.checkBox_wmv.isChecked():
            self.list_filetype.append('.wmv')
        if self.list_filetype == []:
            self.list_filetype = None
        logging.info('list filetype: {}'.format(self.list_filetype))

    def check_search_subdir(self):
        logging.info('Subdir check: {}'.format(self.checkBox_search_subdir.isChecked()))

    def check_execute_option(self):
        # CheckBox & ComboBox & LineEdit Option
        self.dict_execute_option = {'checkBox_save_image': self.checkBox_save_image.isChecked()}
        logging.info('dict_execute_option: {}'.format(self.dict_execute_option))

    def update_tableWidget_filelist_search(self):
        self.label_search_file_count.setText('Searched File(s) : {}'.format(len(self.list_filelist_search)))
        self.tableWidget_filelist_search.setRowCount(len(self.list_filelist_search))
        for cnt, idx_file in enumerate(self.list_filelist_search):
            self.tableWidget_filelist_search.setItem(cnt, 0, QTableWidgetItem(os.path.basename(idx_file)))
            self.tableWidget_filelist_search.setItem(cnt, 1, QTableWidgetItem(os.path.splitext(idx_file)[1]))
            self.tableWidget_filelist_search.setItem(cnt, 2, QTableWidgetItem(os.path.relpath(os.path.dirname(idx_file))))

    def update_tableWidget_filelist_select(self):
        self.label_select_file_count.setText('Selected File(s) : {}'.format(len(self.list_filelist_select)))
        self.tableWidget_filelist_select.setRowCount(len(self.list_filelist_select))
        for cnt, idx_file in enumerate(self.list_filelist_select):
            self.tableWidget_filelist_select.setItem(cnt, 0, QTableWidgetItem(os.path.basename(idx_file)))
            self.tableWidget_filelist_select.setItem(cnt, 1, QTableWidgetItem(os.path.splitext(idx_file)[1]))
            self.tableWidget_filelist_select.setItem(cnt, 2, QTableWidgetItem(os.path.relpath(os.path.dirname(idx_file))))

    #### Make filelist
    def click_btn_search(self):
        self.statusBar().showMessage('Searching files . . .')
        #### -+-+-+-+-+-+-+-+-+- [Search] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- ####
        # File type을 선택하는 Checkbox 정보를 self.list_filetype에 업데이트.
        self.check_search_option()
        logging.info('search file type : {}'.format(self.list_filetype))
        # 하위폴더까지 검색할지에 대한 옵션 확인 후 전체 File list작성
        self.list_filelist_search = make_filelist(target_dir=self.folder_location, subdir=self.checkBox_search_subdir.isChecked(), list_filetype=self.list_filetype)
        logging.debug('File List : {}'.format(self.list_filelist_search))
        # 파일 리스트를 listWidget 목록에 업데이트
        self.clear_search_list()
        self.clear_select_list()
        self.label_view_image.clear()
        self.update_tableWidget_filelist_search()
        write_to_ini(file_name=self.set_file, section_name='History', dict_data={'last folder': self.folder_location})
        self.clear_frame_view()
        #### -+-+-+-+-+-+-+-+-+- [Search] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- ####
        self.statusBar().showMessage('Searching Complete.')

    def click_tableWidget_filelist_search(self):
        self.clear_frame_view()
        # tableWidget의 아이템을 클릭했을때 동작 (단일 파일 선택일 경우만 동작함.)
        self.selected_file_in_search = os.path.abspath(os.path.join(self.tableWidget_filelist_search.item(self.tableWidget_filelist_search.currentRow(), 2).text(),
                                                                    self.tableWidget_filelist_search.item(self.tableWidget_filelist_search.currentRow(), 0).text()))
        # _selected_file = os.path.abspath(self.tableWidget_filelist_search.item(self.tableWidget_filelist_search.currentRow(), 0).text())
        logging.info('filelist_search: [{} ({})] {}'.format(self.selected_file_in_search in self.list_filelist_search,
                                                            self.tableWidget_filelist_search.currentRow(),
                                                            os.path.relpath(self.selected_file_in_search)))
        self.selected_file_info_movie_in_search = get_info_from_movie_file(filename=self.selected_file_in_search)
        self.horizontalSlider_frame_no.setMinimum(1)
        self.horizontalSlider_frame_no.setMaximum(self.selected_file_info_movie_in_search['nFrame'])
        self.horizontalSlider_frame_no.setValue(1)
        self.lineEdit_frame_total.setText(str(self.selected_file_info_movie_in_search['nFrame']))
        logging.info('Movie File Information: {}'.format(self.selected_file_info_movie_in_search))
        self.update_frame_no()
        self.statusBar().showMessage(self.selected_file_in_search)

    def click_tableWidget_filelist_select(self):
        # tableWidget의 아이템을 클릭했을때 동작 (단일 파일 선택일 경우만 동작함.)
        _selected_file = os.path.abspath(os.path.join(self.tableWidget_filelist_select.item(self.tableWidget_filelist_select.currentRow(), 2).text(),
                                                      self.tableWidget_filelist_select.item(self.tableWidget_filelist_select.currentRow(), 0).text()))
        logging.debug('filelist_select: [{} ({})] {}'.format(_selected_file in self.list_filelist_select,
                                                             self.tableWidget_filelist_select.currentRow(),
                                                             os.path.relpath(_selected_file)))
        # self.draw_image_from_file(filename=_selected_file)
        self.statusBar().showMessage(_selected_file)

    def click_btn_add_all(self):
        # self.list_filelist_select를 초기화 한다.
        self.clear_select_list()
        # self.list_filelist_search를 self.list_filelist_select로 복사한다.
        self.list_filelist_select = self.list_filelist_search.copy()
        # 업데이트된 list_filelist_select를 tableWidget_filelist_select에 업데이트
        self.update_tableWidget_filelist_select()

    def click_btn_add(self):
        # 선택된 Search index list를 가져옴.
        _selected_idx_search = [idx.row() for idx in self.tableWidget_filelist_search.selectedIndexes()]
        _selected_idx_search = list(set(_selected_idx_search))
        logging.debug('Search_idx_No.: {}'.format(_selected_idx_search))
        for idx_select in _selected_idx_search:
            # self.list_filelist_select.append(os.path.abspath(os.path.join(self.tableWidget_filelist_search.item(idx_select, 2).text(),
            #                                                               self.tableWidget_filelist_search.item(idx_select, 0).text())))
            # self.list_filelist_select.append(self.tableWidget_filelist_search.item(idx_select, 0).text())
            self.list_filelist_select.append(os.path.abspath(os.path.join(self.tableWidget_filelist_search.item(idx_select, 2).text(),
                                                                          self.tableWidget_filelist_search.item(idx_select, 0).text())))
        self.list_filelist_select = list(set(self.list_filelist_select))
        self.list_filelist_select.sort(reverse=False)
        logging.debug('Selected item : ({}) {}'.format(len(self.list_filelist_select), self.list_filelist_select))
        # 업데이트된 list_filelist_select를 tableWidget_filelist_select에 업데이트
        self.update_tableWidget_filelist_select()

    def click_btn_remove(self):
        # 선택된 Select list를 가져옴.
        _selected_idx_select = [idx.row() for idx in self.tableWidget_filelist_select.selectedIndexes()]
        _selected_idx_select = list(set(_selected_idx_select))
        logging.debug('Select_idx_No.: {}'.format(_selected_idx_select))
        # 선택된 Row Number에 해당하는 파일을 self.list_filelist_select에서 지운다.
        for idx_select in _selected_idx_select:
            self.list_filelist_select.pop(self.list_filelist_select.index(os.path.abspath(os.path.join(self.tableWidget_filelist_select.item(idx_select, 2).text(),
                                                                                                       self.tableWidget_filelist_select.item(idx_select, 0).text()))))
        self.list_filelist_select = list(set(self.list_filelist_select))
        self.list_filelist_select.sort(reverse=False)
        logging.debug('Selected item : ({}) {}'.format(len(self.list_filelist_select), self.list_filelist_select))
        self.update_tableWidget_filelist_select()

    def click_btn_clear(self):
        # self.list_filelist_select를 초기화 한다.
        self.clear_select_list()
        # 업데이트된 list_filelist_select를 tableWidget_filelist_select에 업데이트
        self.update_tableWidget_filelist_select()
    
    def click_tableWidget_roi(self):
        self.lineEdit_roi_start_x.setText(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 0).text())
        self.lineEdit_roi_start_y.setText(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 1).text())
        self.lineEdit_roi_end_x.setText(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 2).text())
        self.lineEdit_roi_end_y.setText(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 3).text())
        self.lineEdit_roi_width.setText(str(int(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 2).text()) - int(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 0).text())))
        self.lineEdit_roi_height.setText(str(int(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 3).text()) - int(self.tableWidget_roi.item(self.tableWidget_roi.currentRow(), 1).text())))
        self.draw_image_from_ndarrary()
    
    def update_tableWidget_roi(self):
        self.tableWidget_roi.setRowCount(len(self.list_roi_select))
        self.tableWidget_roi.setColumnWidth(0, 100)
        self.tableWidget_roi.setColumnWidth(1, 100)
        self.tableWidget_roi.setColumnWidth(2, 100)
        self.tableWidget_roi.setColumnWidth(3, 100)
        for cnt, idx_roi in enumerate(self.list_roi_select):
            self.tableWidget_roi.setItem(cnt, 0, QTableWidgetItem(str(idx_roi[0])))
            self.tableWidget_roi.setItem(cnt, 1, QTableWidgetItem(str(idx_roi[1])))
            self.tableWidget_roi.setItem(cnt, 2, QTableWidgetItem(str(idx_roi[2])))
            self.tableWidget_roi.setItem(cnt, 3, QTableWidgetItem(str(idx_roi[3])))
            
    def click_btn_roi_add(self):
        if (self.lineEdit_roi_start_x.text() == self.lineEdit_roi_end_x.text()) or (self.lineEdit_roi_start_y.text() == self.lineEdit_roi_end_y.text()):
            logging.error('Please Select ROI in image area !!')
        else:
            logging.info('ROI >> Start (X, Y): ({}, {}), End (X, Y): ({}, {})'.format(self.lineEdit_roi_start_x.text(), self.lineEdit_roi_start_y.text(), self.lineEdit_roi_end_x.text(), self.lineEdit_roi_end_y.text()))
            if not ([int(self.lineEdit_roi_start_x.text()), int(self.lineEdit_roi_start_y.text()), int(self.lineEdit_roi_end_x.text()), int(self.lineEdit_roi_end_y.text())] in self.list_roi_select):
                self.list_roi_select.append([int(self.lineEdit_roi_start_x.text()), int(self.lineEdit_roi_start_y.text()), int(self.lineEdit_roi_end_x.text()), int(self.lineEdit_roi_end_y.text())])
            logging.debug('Selected ROI List: {}'.format(self.list_roi_select))


            # # temp startx starty endx endy 화면 비율이 다른 영상을 업로드 했을 때, ui상 드레그한 영역과 실제 선택된 영역이 다른 문제가 있습니다.
            # # 때문에 일시적으로 roi를 직접 선정하여 하드코딩으로 집어넣어서 사용하였습니다.
            # self.list_roi_select.append([583, 235, 729, 376])
            # self.list_roi_select.append([330, 38, 477, 179])
            # self.list_roi_select.append([831, 427, 980, 568])
        self.update_tableWidget_roi()
        
            

    def click_btn_roi_del(self):
        _selected_idx_select = [idx.row() for idx in self.tableWidget_roi.selectedIndexes()]
        _selected_idx_select = list(set(_selected_idx_select))
        logging.debug('Select_roi_idx_No.: {}'.format(_selected_idx_select))
        for idx_select in _selected_idx_select:
            self.list_roi_select.pop(self.list_roi_select.index([int(self.tableWidget_roi.item(idx_select, 0).text()),
                                                                 int(self.tableWidget_roi.item(idx_select, 1).text()),
                                                                 int(self.tableWidget_roi.item(idx_select, 2).text()),
                                                                 int(self.tableWidget_roi.item(idx_select, 3).text())]))
        # self.list_roi_select = list(set(self.list_roi_select))
        self.update_tableWidget_roi()
    
    def click_btn_roi_clear(self):
        self.list_roi_select = []
        self.update_tableWidget_roi()


    def click_btn_execute(self):
        self.statusBar().showMessage('Start Evaluation . . .')
        self.progressBar.setValue(0)
        self.check_execute_option()
        # -+-+-+-+-+-+-+-+-+- [Execute] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- #
        if (len(self.list_filelist_select) == 0) or (len(self.list_roi_select) == 0):
            logging.error('List of file or selected ROI is empty: \n[File] >> ({}) {}\n[ROI] >> ({}) {}'.format(len(self.list_filelist_select), self.list_filelist_select, len(self.list_roi_select), self.list_roi_select))
        else:
            logging.warning('##### Now start evaluation !!! #####')
            # ini에 저장된 기존 사용 Setting 불러오기 - Detection Threshold
            self.detection_threshold = read_from_ini(file_name=self.set_file, section_name='Setting', item='detection threshold')
            if self.detection_threshold == '':
                self.detection_threshold = 30
                write_to_ini(file_name=self.set_file, section_name='Setting', dict_data={'detection threshold': 30})
            else:
                self.detection_threshold = int(self.detection_threshold)
            logging.warning('Detection Threshold: {}'.format(self.detection_threshold))

            for file_cnt, idx_file in enumerate(self.list_filelist_select):
                logging.warning('Video Filename: {} ({})'.format(os.path.basename(idx_file), idx_file))
                result_folder = os.path.dirname(idx_file) + os.sep + '_Result' + os.sep + os.path.splitext(os.path.basename(idx_file))[0] # 엑셀 결과 폴더 만들기
                if not os.path.isdir(result_folder):
                    os.makedirs(result_folder)

                dict_info_video = get_info_from_movie_file(filename=idx_file)
                dict_tracking_data = {}
                if self.checkBox_frame_interval.isChecked():
                    try:#분석 시작 구간 확인
                        _frame_interval_start = int(self.lineEdit_frame_interval_start.text())
                    except:
                        logging.error('Start of interval is empty. >> set to 1')
                        _frame_interval_start = 1

                    if _frame_interval_start < 1:
                        logging.error('Start of interval is smaller than 1.: {}'.format(_frame_interval_start))
                        _frame_interval_start = 1
                    elif _frame_interval_start > dict_info_video['nFrame']:
                        logging.error('Start of interval is bigger than number of frame. >>> Interval Start: {} (Number of frame: {})'.format(_frame_interval_start, dict_info_video['nFrame']))
                        _frame_interval_start = dict_info_video['nFrame']
                    else:
                        logging.info('Interval start : {}'.format(_frame_interval_start))

                    try: # 분석 끝 구간 확인
                        _frame_interval_end = int(self.lineEdit_frame_interval_end.text())
                    except:
                        _frame_interval_end = _frame_interval_start
                        logging.error('End of interval is empty. >> set to start of interval')

                    if _frame_interval_end < _frame_interval_start:
                        logging.error('End of interval is smaller than start. >>> Interval End: {} (Interval Start: {})'.format(_frame_interval_end, _frame_interval_start))
                        _frame_interval_end = _frame_interval_start
                    elif _frame_interval_end > dict_info_video['nFrame']:
                        logging.error('End of interval is bigger than end frames. >> Interval End: {} (Number of end frame: {})'.format(_frame_interval_end, dict_info_video['nFrame']))
                        _frame_interval_end = dict_info_video['nFrame']
                    else:
                        logging.info('Interval end : {}'.format(_frame_interval_end))
                else:
                    _frame_interval_start = 1
                    _frame_interval_end = dict_info_video['nFrame']
                logging.warning('[{}] Interval set from {} to {}'.format(os.path.basename(idx_file), _frame_interval_start, _frame_interval_end))

                for frame_cnt in range(_frame_interval_start, _frame_interval_end + 1): # 지정된 프레임 범위에서
                    frame_org, _, frame_width, frame_height = extraction_frame(filename=idx_file, frame_no=frame_cnt) # Frame 추출하는 부분
                    if frame_width == None: # oppo 에서 프레임 읽어오지 못하는 문제가 있음 이를 해결하는 방법은 아직 모르겠으나 예외처리는 해둠
                        continue
                    else:
                        logging.debug('[{}] Extrect frame >> Frame No.: {}, Frame Shape: {}'.format(os.path.basename(idx_file), frame_cnt, np.shape(frame_org)))
                        frame_full = frame_org.copy()
                        # frame_crop = frame_org.copy()

                        for roi_cnt, axis_roi in enumerate(self.list_roi_select): # 선택한 각각의 ROI에 대하여
                            if not(roi_cnt in dict_tracking_data.keys()):
                                dict_tracking_data[roi_cnt] = {'Frame_No': [],
                                                               'ROI_No': [],
                                                               "Image_Height" : [],
                                                               "Image_Width" : [],
                                                               'ROI_Start_X': [],
                                                               'ROI_Start_Y': [],
                                                               'ROI_End_X': [],
                                                               'ROI_End_Y': [],
                                                               'Marker_Center_X_crop': [],
                                                               'Marker_Center_Y_crop': [],
                                                               'Marker_Center_X_full': [],
                                                               'Marker_Center_Y_full': [],
                                                               'Marker_Width': [],
                                                               'Marker_Height': []}
                            logging.debug('Filename: {}, Frame_No.: {}, ROI No.: {}, ROI Start: ({}, {}), ROI End: ({}, {})'.format(os.path.basename(idx_file), frame_cnt, roi_cnt, axis_roi[0], axis_roi[1], axis_roi[2], axis_roi[3]))
                            # frame_roi, dict_axis = DetectionMark(img=frame_org.copy(), axisStart=[axis_roi[0], axis_roi[1]], axisEnd=[axis_roi[2], axis_roi[3]], threshold=self.detection_threshold) # 선택한 roi 내에 마크 탐색
                            frame_roi, dict_axis = DetectionMark(file=idx_file, frame_no=frame_cnt, img=frame_org.copy(), save = self.dict_execute_option['checkBox_save_image'])
                            if not dict_axis:
                                continue
                            if self.dict_execute_option['checkBox_save_image']: # 이미지 저장시
                                cv2.imwrite(filename=result_folder + os.sep + os.path.splitext(os.path.basename(idx_file))[0] + '_ROI ' + str(roi_cnt) + '_Frame_' + str(frame_cnt) + '.png', img=frame_roi)

                                cv2.rectangle(img=frame_full, pt1=(axis_roi[0], axis_roi[1]), pt2=(axis_roi[2], axis_roi[3]), color=(255, 0, 0), thickness=2, lineType=cv2.LINE_8)
                                cv2.putText(img=frame_full, text='ROI #' + str(roi_cnt), org=(axis_roi[0], axis_roi[1] - 3), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(255, 0, 0), thickness=2, lineType=8)
                                cv2.line(img=frame_full, pt1=(int(np.shape(frame_full)[1] / 2), 0), pt2=(int(np.shape(frame_full)[1] / 2), np.shape(frame_full)[0]), color=(0, 0, 255), thickness=1)
                                cv2.line(img=frame_full, pt1=(0, int(np.shape(frame_full)[0] / 2)), pt2=(np.shape(frame_full)[1], int(np.shape(frame_full)[0] / 2)), color=(0, 0, 255), thickness=1)
                                cv2.imwrite(filename=result_folder + os.sep + os.path.splitext(os.path.basename(idx_file))[0] + '_Frame_' + str(frame_cnt) + '.png', img=frame_full)

                            for idx_roi in dict_axis.keys():
                                dict_tracking_data[roi_cnt]['Frame_No'].append(frame_cnt)
                                dict_tracking_data[roi_cnt]['ROI_No'].append(idx_roi)
                                dict_tracking_data[roi_cnt]['Image_Height'].append(frame_height)
                                dict_tracking_data[roi_cnt]['Image_Width'].append(frame_width)
                                dict_tracking_data[roi_cnt]['ROI_Start_X'].append(axis_roi[0])
                                dict_tracking_data[roi_cnt]['ROI_Start_Y'].append(axis_roi[1])
                                dict_tracking_data[roi_cnt]['ROI_End_X'].append(axis_roi[2])
                                dict_tracking_data[roi_cnt]['ROI_End_Y'].append(axis_roi[3])
                                dict_tracking_data[roi_cnt]['Marker_Center_X_crop'].append(dict_axis[idx_roi]['center_x'])
                                dict_tracking_data[roi_cnt]['Marker_Center_Y_crop'].append(dict_axis[idx_roi]['center_y'])
                                dict_tracking_data[roi_cnt]['Marker_Center_X_full'].append(axis_roi[0] + dict_axis[idx_roi]['center_x'])
                                dict_tracking_data[roi_cnt]['Marker_Center_Y_full'].append(axis_roi[1] + dict_axis[idx_roi]['center_y'])
                                dict_tracking_data[roi_cnt]['Marker_Width'].append(dict_axis[idx_roi]['x_max'] - dict_axis[idx_roi]['x_min'] + 1)
                                dict_tracking_data[roi_cnt]['Marker_Height'].append(dict_axis[idx_roi]['y_max'] - dict_axis[idx_roi]['y_min'] + 1)

                                logging.debug('Frame No.: {}/{} >> ROI No.: {} >> Center axis(X, Y): ({}, {})'.format(frame_cnt, dict_info_video['nFrame'], idx_roi, dict_axis[idx_roi]['center_x'], dict_axis[idx_roi]['center_y']))
                            logging.debug('Tracking Data (ROI # {}): {}'.format(roi_cnt, dict_tracking_data))

                for roi_result_cnt in range(len(dict_tracking_data)):
                    df_tracking_data = pd.DataFrame.from_dict(dict_tracking_data[roi_result_cnt])
                    if len(df_tracking_data) != 0:
                        result_filename = result_folder + os.sep + 'Result_' + os.path.splitext(os.path.basename(idx_file))[0] + '_ROI_' + str(roi_result_cnt) + '.xlsx'
                        with pd.ExcelWriter(result_filename) as writer:
                            df_tracking_data.to_excel(writer, sheet_name='ALL')
                            # for idx_roi in range(max(df_tracking_data['ROI_No']) + 1):
                            #     df_tracking_data[df_tracking_data['ROI_No'] == idx_roi].to_excel(writer, sheet_name='ROI_' + str(idx_roi))
                        logging.warning('Result data of [{}] is saved to [{}]'.format(os.path.basename(idx_file), os.path.basename(result_filename)))
                self.progressBar.setValue(int((file_cnt + 1) / len(self.list_filelist_select) * 100))
        # -+-+-+-+-+-+-+-+-+- [Execute] 버튼 클릭시 수행할 내용 -+-+-+-+-+-+-+-+-+- #
        # ini 파일에 업데이트
        write_to_ini(file_name=self.set_file,
                     section_name='History',
                     dict_data={'last folder': self.folder_location})
        self.statusBar().showMessage('Complete Evaluation . . .')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    sys.exit(app.exec_())
