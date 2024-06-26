from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2,imutils
import sys

class MyThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            _,frame = self.cap.read()
            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)
    
    def cvimage_to_label(self,image):
        image = imutils.resize(image,width = 640)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = QImage(image,
                       image.shape[1],
                       image.shape[0],
                       QImage.Format_RGB888)
        return image

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()
    
    def init_ui(self):
        self.setFixedSize(640,640)
        self.setWindowTitle("Camera FeedBack")

        widget = QWidget(self)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.open_btn = QPushButton("Open The Camera", clicked=self.open_camera)
        layout.addWidget(self.open_btn)

        self.camera_thread = MyThread()
        self.camera_thread.frame_signal.connect(self.setImage)

        self.setCentralWidget(widget)
    
    def open_camera(self):        
        self.camera_thread.start()
        print(self.camera_thread.isRunning())

    @pyqtSlot(QImage)
    def setImage(self,image):
        self.label.setPixmap(QPixmap.fromImage(image))



if __name__ == "__main__":
    app = QApplication([])
    main_window = MainApp()
    sys.exit(app.exec())