from Gui import face_recognition_system
import sys


if __name__ == '__main__':
    app = face_recognition_system.QApplication(sys.argv)
    w = face_recognition_system.FaceRecognitionSystem()
    w.show()
    sys.exit(app.exec())
