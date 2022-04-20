import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType('manage.ui')[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.crawling_btn.clicked.connect(self.crawling_btn_clicked)
        self.detection_btn.clicked.connect(self.detection_btn_clicked)
        self.recognition_btn.clicked.connect(self.recognition_btn_clicked)
        self.log_btn.clicked.connect(self.log_btn_clicked)
        
        self.crawling_dir_btn.clicked.connect(self.crawling_dir_btn_clicked)
        self.detection_dir_btn.clicked.connect(self.detection_dir_btn_clicked)
        self.recognition_dir_btn.clicked.connect(self.recognition_dir_btn_clicked)
        self.log_dir_btn.clicked.connect(self.log_dir_btn_clicked)
        
        self.log_txt
    
    
    def crawling_btn_clicked(self):
        print('crawling')
        
    def detection_btn_clicked(self):
        print('detection')
        
    def recognition_btn_clicked(self):
        print('recognition')
        
    def log_btn_clicked(self):
        print('log')
    
    def crawling_dir_btn_clicked(self):
        print('crawling dir')
        
    def detection_dir_btn_clicked(self):
        print('detection dir')
        
    def recognition_dir_btn_clicked(self):
        print('recognition dir')
        
    def log_dir_btn_clicked(self):
        print('log dir')


if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    main_window = WindowClass() 
    main_window.show()

    app.exec_()