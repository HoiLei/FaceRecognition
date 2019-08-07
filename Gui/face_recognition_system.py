# coding utf-8
import os
import cv2
import time
import datetime
import pickle
import threading
from imutils import paths
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import face_recognition     # 基于Dlib的人脸识别包
import recognize0
import md_encodings


# 主窗口类
class FaceRecognitionSystem(QWidget):
    # 初始函数
    def __init__(self, parent=None):
        super(FaceRecognitionSystem, self).__init__(parent)
        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture()
        self.set_ui()
        self.cap_num = 0
        self.slot_init()
        self.btn_flag = 0

    # 设置图形界面
    def set_ui(self):
        # 布局和按钮
        self.layout_main = QHBoxLayout()
        self.layout_button = QVBoxLayout()
        self.btn_open_cam = QPushButton('打开摄像')
        self.btn_input_face = QPushButton('录入人脸')
        self.btn_detection = QPushButton('人脸检测')
        self.btn_encodings = QPushButton('人脸编码')
        self.btn_recognition = QPushButton('人脸识别')
        self.btn_quit = QPushButton('退出系统')

        # 显示视频
        self.label_show_camera = QLabel()
        self.label_move = QLabel()
        self.label_move.setFixedSize(100, 200)
        self.label_show_camera.setFixedSize(800, 600)
        self.label_show_camera.setAutoFillBackground(False)

        self.text = QTextBrowser()

        # 设置布局
        self.layout_button.addWidget(self.btn_open_cam)
        self.layout_button.addWidget(self.btn_input_face)
        self.layout_button.addWidget(self.btn_detection)
        self.layout_button.addWidget(self.btn_encodings)
        self.layout_button.addWidget(self.btn_recognition)
        self.layout_button.addWidget(self.btn_quit)
        self.layout_button.addWidget(self.label_move)
        self.layout_button.addWidget(self.text)
        self.layout_main.addLayout(self.layout_button)
        self.layout_main.addWidget(self.label_show_camera)
        self.setLayout(self.layout_main)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("人脸识别系统")

    # 信号槽绑定
    def slot_init(self):
        self.btn_open_cam.clicked.connect(self.btn_open_cam_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.btn_input_face.clicked.connect(self.input_face)
        self.btn_detection.clicked.connect(self.btn_detection_face)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_encodings.clicked.connect(self.btn_encodings_click)
        self.btn_recognition.clicked.connect(self.btn_recognize_face)

    # 打开摄像头按钮
    def btn_open_cam_click(self):
        if self.timer_camera.isActive() is False:
            flag = self.cap.open(self.cap_num)
            if flag is False:
                msg = QMessageBox.warning(self, u"Warning", u"请检测摄像头是否连接正确",
                                          buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.btn_open_cam.setText("关闭摄像")
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.btn_open_cam.setText("打开摄像")

    # 显示摄像头视频
    def show_camera(self):
        # 正常显示摄像头画面
        if self.btn_flag == 0:
            ret, self.image = self.cap.read()
            show = cv2.resize(self.image, (800, 600))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            self.showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QPixmap.fromImage(self.showImage))
        # 显示人脸检测画面
        if self.btn_flag == 1:
            ret1, self.image_1 = self.cap.read()
            show_0 = cv2.resize(self.image_1, (0,0), fx=0.5, fy=0.6)
            show_1 = cv2.cvtColor(show_0, cv2.COLOR_BGR2RGB)
            # 进行人脸检测
            faces = face_recognition.face_locations(show_1)
            # 绘制矩形框
            for (top, right, bottom, left) in faces:
                cv2.rectangle(show_1, (left, top), (right, bottom), (0, 255, 0), 2)
            # 把图像转化为QT能显示的QImage
            detect_image = QImage(show_1.data, show_1.shape[1], show_1.shape[0],
                                  QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QPixmap.fromImage(detect_image))
        # 显示人脸识别画面
        if self.btn_flag == 2:
            ret2, self.image_2 = self.cap.read()
            show_2 = cv2.resize(self.image_2, (0,0), fx=0.25, fy=0.25)
            show_3 = cv2.cvtColor(show_2, cv2.COLOR_BGR2RGB)
            recognize0.recognize(show_3)    #进行人脸识别
            detect_image = QImage(show_3.data, show_3.shape[1], show_3.shape[0],
                                  QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QPixmap.fromImage(detect_image))

    # 录入人脸
    def input_face(self):
        count = 1
        # 输入人名
        text, ok = QInputDialog.getText(self, '数据录入', '请输入名字后旋转脸部：')
        # 创建人名目录
        if ok:
            path = './DataSet/' + text
            path = path.strip()     # 去除首位空格
            path = path.rstrip()    # 去除尾部'/'
            is_exists = os.path.exists(path)
            # 如果目录下不存在以该人名命名文件夹则创建一个
            if not is_exists:
                os.makedirs(path)
            photo_save_path = os.path.join(os.path.dirname(os.path.abspath('__file__')),
                                           path + '/')
            # 使用循环结构达到延时目的，约1秒存储一张图像
            for i in range(0, 500, 5):
                # 开启多线程，为了存储图像同时不影响画面显示
                t = threading.Thread(self.show_camera())
                t.setDaemon(True)
                t.start()
                QApplication.processEvents()
                if i % 50 == 0:
                    self.showImage.save(photo_save_path +
                                        datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg")
                    self.send_str('Saving image['+str(count)+']')
                    count += 1
            self.send_str("Succeed")
            self.encodings(path)

    # 用于绑定编码按钮的函数，对数据库所有图像进行编码
    def btn_encodings_click(self):
        self.encodings('DataSet')

    # 编码函数，输入为图像路径
    def encodings(self, img_path):
        image_paths = list(paths.list_images(img_path))     # 读取路径下所有图像文件
        known_encodings = []    # 编码字典
        known_names = []        # 人名字典
        for(i, image_path) in enumerate(image_paths):
            str = "processing image {}/{}".format(i+1, len(image_paths))
            # 开启多线程同时显示编码进度
            t = threading.Thread(self.send_str(str))
            t.setDaemon(True)
            t.start()
            QApplication.processEvents()
            md_encodings.func_encodings(image_path, known_encodings, known_names)
        self.send_str('Saving the encodings...')
        data = {"encodings": known_encodings, "names": known_names}   # 数据字典
        f = open("encodings", "wb")       # 写入编码数据
        f.write(pickle.dumps(data))             # 保存为pickle文件
        f.close()
        self.send_str('Finished')

    # 用于切换状态函数
    def btn_detection_face(self):
        if self.btn_flag == 0 or self.btn_flag == 2:
            self.btn_flag = 1
            self.btn_detection.setText('关闭检测')
        elif self.btn_flag == 1:
            self.btn_flag = 0
            self.btn_detection.setText('人脸检测')

    # 在文本框发送字符
    def send_str(self, t):
        self.text.append(t)
        self.text.moveCursor(self.text.textCursor().End)
        time.sleep(0.2)

    # 人脸识别状态切换
    def btn_recognize_face(self):
        if self.btn_flag == 0 or self.btn_flag == 1:
            self.btn_flag = 2
            self.btn_recognition.setText('关闭识别')
        elif self.btn_flag == 2:
            self.btn_flag = 0
            self.btn_recognition.setText('人脸识别')
