import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PIL import Image

from multiprocessing import Process

import crawling
import detection

crawling_process = Process(target=crawling.main)
detection_process = Process(target=detection.main)

form_class = uic.loadUiType('manage.ui')[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.file_exp_btn.clicked.connect(self.file_exp_btn_clicked)
        self.run_btn.clicked.connect(self.run_btn_clicked)
        self.leak_btn.clicked.connect(self.leak_btn_clicked)
        self.report_btn.clicked.connect(self.report_btn_clicked)
        
        self.capture_btn.clicked.connect(self.capture_btn_clicked)
        self.capture_btn.setStyleSheet("background-image : url(cap.png);")
        
        self.temp_file_txt
        self.log_txt.append(f"[*] Management program start")
        self.log_txt.append(f"[*] Continue to Image crawling")
        self.log_txt.append(f"[*] Continue to RoI cropping")
        
        crawling_process.start(); 
        detection_process.start();
        
        
    def file_exp_btn_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            try:
                Image.open(fname[0])
                self.temp_file_txt.setPlainText(fname[0])
            except IOError:
                QMessageBox.about(self, 'Error', '유효하지 않은 이미지 입니다.')
    
    
    def capture_btn_clicked(self):
        # 인터넷 브라우저 만들기
        pass
    
    
    def run_btn_clicked(self):
        if self.temp_file_txt.toPlainText() == '사진 업로드 필요 !!':
            QMessageBox.about(self, 'Error', '먼저 사진을 업로드 하셔야 합니다.')
            return
        
        self.temp_file_txt.setPlainText('사진 업로드 필요 !!')
        
        self.log_txt.append(f"[*] Start to Recognition")
    
    
    def leak_btn_clicked(self):
        pass
    
    
    def report_btn_clicked(self):
        pass
    
    


if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    main_window = WindowClass() 
    main_window.show()

    app.exec_()