import json
import cv2
import face_recognition
import numpy as np
from PyQt5 import QtCore

class MatcherThread(QtCore.QThread):
    match_result_signal = QtCore.pyqtSignal(dict)  # 用于通知匹配结果

    def __init__(self, feature_vector_list, detection_results_queue, match_type):
        super().__init__()
        self.feature_vector_list = feature_vector_list
        self.detection_results_queue = detection_results_queue
        self.match_type = match_type

    @staticmethod
    def q_image_transform(image, k):
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        # 创建 NumPy 数组，并重塑为 (height, width, 3)形状
        cv_image = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, 3))
        # 将 BGR 转为 RGB（适用于 face_recognition）
        if k == 0:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        return rgb_image

    def parse_identity_codes(self, identity_codes):  
        # 将字符串解析为实际的列表
        return [json.loads(code) for code in identity_codes]

    def run(self):
        if self.match_type == 0:  # 匹配人脸
            if self.feature_vector_list:
                identity_codesx = [reservation[2] for reservation in self.feature_vector_list]
                identity_codes = self.parse_identity_codes(identity_codesx)

                frames = []
                for _ in range(4):
                    u = self.detection_results_queue.get()["q_image"]
                    frames.append(self.q_image_transform(u, 0))

                matched_identity_codes = []
                for i in frames:
                    # 查找当前帧中的人脸
                    face_locations = face_recognition.face_locations(i)
                    # 检查人脸
                    if face_locations:
                        face_encoding = face_recognition.face_encodings(
                            i, face_locations, num_jitters=1
                        )[0]
                        # 对比identity_codes与用户的face_encoding
                        results = face_recognition.compare_faces(identity_codes, face_encoding,0.6)
                        index = 0
                        for s in results:
                            if s:
                                matched_identity_codes.append(
                                    (
                                        self.feature_vector_list[index][0],
                                        self.feature_vector_list[index][1]
                                    )
                                )
                            index += 1
                            if matched_identity_codes:
                                break
                    if matched_identity_codes:
                        break
                self.match_result_signal.emit({"type": 0,"result": matched_identity_codes})
            else:
                self.match_result_signal.emit({"type": 2, "result": "当前时段没有与预约记录匹配的面部信息，请确认。"})

        else:  # 匹配二维码
            qrcode = ""
            detector = cv2.QRCodeDetector()
            for _ in range(4):
                self.match_result_signal.emit({"type": 10, "result": "正在检测"})
                u = self.detection_results_queue.get()["q_image"]
                rgb_image = self.q_image_transform(u, 1)
                decoded_text, points, l  = detector.detectAndDecode(rgb_image)

                if decoded_text:
                    self.match_result_signal.emit({"type": 10, "result": f"已完成解码-{decoded_text}"})
                    qrcode += decoded_text
                    break

            self.match_result_signal.emit({"type": 1, "result": qrcode})

        #  结束信号
        self.match_result_signal.emit({"type": 12})
