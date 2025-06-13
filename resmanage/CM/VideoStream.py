import cv2
from PyQt5 import QtCore, QtGui

class VideoThread(QtCore.QThread):
    image_ready = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.qr_detector = cv2.QRCodeDetector()

    def run(self):
        cap = cv2.VideoCapture(0)
        # 设置视频流的宽度和高度
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        frame_count = 0

        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break  # 如果无法读取帧，退出循环

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = False  # 标记检测到的人脸
            qr_code_detected = False  # 标记二维码
            need_prop = False

            # 每12次循环检测
            if frame_count % 12 == 0:
                need_prop = True
                points = self.qr_detector.detect(gray)  # 进行二维码检测
                if points[0]:
                    qr_code_detected = True

                if not qr_code_detected:
                    # 进行人脸检测
                    faces = self.face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=4,
                        flags=cv2.CASCADE_FIND_BIGGEST_OBJECT,
                        minSize=(80, 80),
                        maxSize=(460, 460)
                    )
                    if len(faces) > 0:
                        faces_detected = True  # 有检测到的人脸
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (173, 255, 47), 2)  # 绘制人脸矩形框

            # 转换为 RGB 格式并发出信号
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

            # 每次循环发出信号，包含二维码和人脸的检测状态
            self.image_ready.emit({
                "need_prop": need_prop,
                "image": q_image,
                "faces_detected": faces_detected,
                "qr_code_detected": qr_code_detected
            })

            self.msleep(36)  # Sleep for 36 ms
            frame_count += 1
        cap.release()

    def start_stream(self):
        if not self.is_running:
            self.start()
        self.is_running = True

    def stop_stream(self):
        if self.isRunning():
            self.stop()
        self.is_running = False
