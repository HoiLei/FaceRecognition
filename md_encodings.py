# coding utf-8
import os
import face_recognition
import cv2


def func_encodings(image_path, known_encodings, known_names):
    name = image_path.split(os.path.sep)[-2]     # 读取路径中文件夹名，并分隔出人名
    image = cv2.imread(image_path)               # opencv读取图像函数读出图像为bgr形式
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    # dlib库要求输入图像为rgb形式

    # 检测出人脸，返回人脸边框数组
    boxes = face_recognition.face_locations(rgb)
    # 对面部数据编码得到128个特征值列表
    encodings = face_recognition.face_encodings(rgb, boxes)
    # 在列表中循环，往已知编码和已知人名列表中插入得到的数据
    for encoding in encodings:
        known_encodings.append(encoding)
        known_names.append(name)
