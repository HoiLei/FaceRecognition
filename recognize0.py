# coding utf-8
import face_recognition
import pickle
import cv2
from Gui import face_recognition_system



def recognize(img):
    fas = face_recognition_system.FaceRecognitionSystem()
    fas.send_str('loading encodings...')
    data = pickle.loads(open("./encodings", "rb").read())   # 读入编码数据
    rgb = cv2.cvtColor(img,  cv2.COLOR_BGR2RGB)
    fas.send_str("recognizing faces...")
    boxes = face_recognition.face_locations(rgb)    # 人脸检测
    encodings = face_recognition.face_encodings(rgb, boxes) # 人脸编码
    names = []
    for encoding in encodings:

        # 与候选编码进行比较，返回值为True或False
        matches = face_recognition.compare_faces(data["encodings"],
                                             encoding)
        name = "Unknown"    # 名字默认为未知

        # 如果为真，得到该编码的索引
        if True in matches:
            matched_idxs = [i for(i, b) in enumerate(matches) if b]
            counts = {}

            # 得到对应人名
            for i in matched_idxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)
        names.append(name)

    # 用zip把边框数组和对应人名打包成元组列表
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)      # 绘制边框
        y = top + 15
        cv2.putText(img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)           # 标出人名
