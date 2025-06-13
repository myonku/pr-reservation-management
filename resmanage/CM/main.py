# -*- coding: utf-8 -*-

"""
已知bug：从后端服获取多个向量时（也就是同时段内有多条个人纪录）传来的文本转json会处理出错，
（单个没问题），推断是list嵌套和str转换的基础问题
"""

import json
import queue
from datetime import datetime
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets

from FaceMatch import MatcherThread
from Socket import SocketThread
from VideoStream import VideoThread


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()  # 不一定需要
        # 创建视频流线程实例
        self.queue_reachable = True
        self.matcher_thread = None
        self.video_thread = VideoThread()
        # 实例化 SocketThread
        self.socket_thread = SocketThread()
        self.feature_vector_list = []  #保存向量列表到内存中
        self.datatime = None  #设置保存时间检查过期
        self.detection_results_queue = queue.Queue()  # 用于存储检测结果
        self.device = "测试1"

        self.MainWindow = QtWidgets.QMainWindow()  # 创建 MainWindow 实例
        self.setupUi()
        self.connect_signals()
        # WebSocket相关属性

    def setupUi(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setFixedSize(950, 600)
        self.MainWindow.setWindowTitle("测试客户端")
        self.MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.MainWindow.setCentralWidget(self.centralwidget)

        # 列表框
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(20, 10, 291, 551)

        # 连接和断开按钮
        self.pushButton = QtWidgets.QPushButton("连接服务器", self.centralwidget)
        self.pushButton.setGeometry(50, 30, 241, 41)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton_2 = QtWidgets.QPushButton("断开连接", self.centralwidget)
        self.pushButton_2.setGeometry(50, 80, 241, 41)

        # 文本浏览器
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(50, 210, 241, 331)

        # 显示图像的标签
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(360, 10, 551, 551)
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")

        # 输入框
        self.lineEdit = QtWidgets.QLineEdit(self.MainWindow)
        self.lineEdit.setGeometry(50, 140, 120, 41)  # 将宽度设置为 120 像素
        self.lineEdit.setPlaceholderText("输入服务器地址")  # 提示文本
        self.lineEdit.setStyleSheet("QLineEdit { text-align: center; }")
        self.lineEdit.setText("127.0.0.1")  # 预设的默认输入值

        # 选择框
        self.comboBox = QtWidgets.QComboBox(self.MainWindow)
        self.comboBox.setGeometry(180, 140, 110, 41)  # 将选择框设置为 120 像素宽且与输入框对齐
        self.comboBox.addItems(["测试1", "测试2", "测试3", "测试4", "测试5", "测试6"])  # 添加选择项
        self.comboBox.setStyleSheet("QComboBox { text-align: center; }")
        # 连接选择框的变化信号到一个自定义的槽函数
        self.comboBox.currentIndexChanged.connect(self.update_device)

        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.MainWindow.setStatusBar(self.statusbar)

        # 翻译界面元素
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "连接服务器"))
        self.pushButton_2.setText(_translate("MainWindow", "断开连接"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    # 子线程信号绑定
    def connect_signals(self):
        self.video_thread.image_ready.connect(self.handle_image_data)
        self.socket_thread.message_received.connect(self.handle_socket_data)
        self.pushButton.clicked.connect(self.connect_to_server)
        self.pushButton_2.clicked.connect(self.disconnect_from_server)
        # 连接选择框的信号

    def update_device(self):
        self.feature_vector_list = None
        self.device = self.comboBox.currentText()
        self.socket_thread.device = self.device
        yr = self.socket_thread.isRunning()
        if yr:
            self.disconnect_from_server()
        self.display_message("已切换到设备：{}".format(self.device))
        self.update_socket_url()
        if yr:
            self.connect_to_server()

    def update_socket_url(self):
        # 获取选择框中的当前URL并更新socket_thread的url
        if_is_running = self.socket_thread.isRunning()
        url = self.lineEdit.text()
        if if_is_running:
            self.disconnect_from_server()
            self.video_thread.stop_stream()

        self.socket_thread.update_url(url)
        self.display_message(f"当前地址：{url}")
        if if_is_running:
            self.connect_to_server()

    def connect_to_server(self):
        url = self.lineEdit.text()
        self.socket_thread.update_url(url)
        if not self.socket_thread.isRunning():
            try:
                self.socket_thread.start_connection()
            except Exception as e:
                self.display_message(f"服务启动失败: {str(e)}")
            self.start_video_stream()
        else:
            self.display_message("已处于连接状态。")

    def disconnect_from_server(self):
        self.video_thread.is_running = False
        if self.socket_thread.isRunning():
            self.socket_thread.stop_connection()
        else:
            self.display_message("未处于连接状态。")
        self.socket_thread.running = False
        while self.video_thread.isRunning() or self.matcher_thread:
            sleep(0.4)
        self.label.clear()
        sleep(0.2)
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.feature_vector_list = None
        self.datatime = None

    def update_feature_data(self):
        current_time = datetime.now()
        client_time = datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")
        if self.datatime is None or self.feature_vector_list is None:
            # 如果datatime为None，表示还没有保存时间，直接更新
            self.datatime = current_time
            self.socket_thread.send_message({"type":0,"client_time":client_time,"device":self.device})  # 调用socket线程更新列表
            return

            # 检查当前时间和保存时间是否在同一个小时段
        same_hour = (
            current_time.year == self.datatime.year and
            current_time.month == self.datatime.month and
            current_time.day == self.datatime.day and
            current_time.hour == self.datatime.hour
        )

        # 如果不在同一个小时段，则更新向量列表
        if not same_hour:
            self.datatime = current_time  # 更新保存时间

            self.socket_thread.send_message({"type":0,"client_time":client_time,"device":self.device})  # 调用socket线程更新列表

    def handle_socket_data(self, message):
        """处理socket线程服务器返回数据"""
        try:
            data = json.loads(message)
            datatype = data["type"]
            if datatype == "type1_response":
                self.feature_vector_list = data["reservations"]  # 获取向量列表

            elif datatype == "type2_response":
                if data["status"] == "confirmed":
                    self.display_message("未找到当前时间段/通道相关的预约申请记录。")
                elif data["status"] == "error":
                    self.display_message("验证失败，内部发生错误。")
                elif data["status"] == "empty":
                    self.display_message("您于当前时间段的申请已经全部通过，请勿重复尝试。")
                elif data["status"] == "success":
                    username = data["username"]
                    match_time = data["match_time"]
                    self.display_message(f"验证成功：用户{username}于{match_time}通过验证。")

            elif datatype == "type3_response":
                if data["status"] == "success":
                    username = data["username"]
                    match_time = data["match_time"]
                    self.display_message(f"验证成功：用户{username}于{match_time}通过验证。")
                elif data["status"] == "error":
                    self.display_message("验证失败，内部发生错误。")
                elif data["status"] == "empty":
                    self.display_message("您于当前时间段的申请已经全部通过，请勿重复尝试。")
                elif data["status"] == "none":
                    if data["username"]:
                        self.display_message("未找到当前时间段/通道相关的预约申请记录。")
                    else:
                        self.display_message("验证失败，未找到相关用户。")
        except json.JSONDecodeError:
            self.display_message(message)

    def handle_image_data(self, message):
        """处理视频流线程的信号"""
        cfr = 4                                    #  控制检测目标次数
        q_image = message["image"]
        need_prop = message["need_prop"]
        if self.queue_reachable and need_prop:
            faces_detected = message["faces_detected"]
            qr_code_detected = message["qr_code_detected"]

            # 存储检测到的结果
            if self.detection_results_queue.qsize() >= cfr:
                self.detection_results_queue.get()  # 移除最旧的

            # 加入新的检测结果
            self.detection_results_queue.put(
                {
                    "q_image": q_image,
                    "faces_detected": faces_detected,
                    "qr_code_detected": qr_code_detected
                }
            )  # 加入新的
            if self.detection_results_queue.qsize() == cfr:
                last_four_results = list(self.detection_results_queue.queue)[-cfr:]
                faces_detected_list = [result["faces_detected"] for result in last_four_results]
                qr_code_detected_list = [result["qr_code_detected"] for result in last_four_results]
                # 检查是否所有的faces_detected都是True
                if all(faces_detected_list):
                    self.queue_reachable = False
                    self.display_message("检测到面部，尝试更新特征数据集。")
                    self.update_feature_data()
                    self.display_message("更新特征特征数据集成功。")
                    self.start_matching_thread(0)   # 调用匹配线程并传递参数 0，代表基于人脸匹配
                # 检查是否所有的qr_code_detected都是True
                elif all(qr_code_detected_list):  # 调用匹配线程并传递参数 1，代表基于二维码匹配
                    self.queue_reachable = False
                    self.display_message("确认检测到二维码。")
                    self.start_matching_thread(1)

            # 更新 GUI 显示
        self.update_image(q_image)

    def start_matching_thread(self, match_type):
        """启动匹配线程的方法"""
        child_detection_results_queue = queue.Queue()
        while not self.detection_results_queue.empty():
            item = self.detection_results_queue.get()  # 从主线程队列中获取元素
            child_detection_results_queue.put(item)  # 放入新的队列
        self.display_message("正在初始化匹配线程。")
        self.matcher_thread = MatcherThread(
            self.feature_vector_list,
            child_detection_results_queue,
            match_type,
        )
        self.display_message("初始化成功，正在启动匹配...")
        # 连接信号以及启动线程
        self.matcher_thread.match_result_signal.connect(self.handle_match_result)
        self.matcher_thread.start()

        # self.detection_results_queue.queue.clear()  # 清空队列

    def handle_match_result(self, message):
        """处理匹配线程的消息"""
        if message["type"] == 0:
            face_result = message["result"][0]
            if face_result:
                self.display_message(f"识别到用户：{face_result[1]}，正在向服务器确认。")
                self.socket_thread.send_message({"type":1, "match_result":True,"id":face_result[0]})
            else:
                self.display_message("未能匹配到用户。")
        elif message["type"] == 1:

            qr_result = message["result"]
            if qr_result:
                client_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                self.display_message("二维码解析成功，正在向服务器确认。")
                self.socket_thread.send_message(
                    {
                        "type":2,
                        "qrcode":qr_result,
                        "device":self.device,
                        "client_time": client_time
                    }
                )
            else:
                self.display_message("二维码解析失败。")
        elif message["type"] == 2:
            self.display_message(message["result"])
        elif message["type"] == 12:
            self.stop_matcher_thread()
        else:
            self.display_message(message["result"])

    def stop_matcher_thread(self):
        if self.matcher_thread:
            try:
                self.matcher_thread = None
            finally:
                self.queue_reachable = True
        self.queue_reachable = True

    def display_message(self, message):
        self.textBrowser.append(message)
        # 获取文本浏览器中所有文本的行数
        lines = self.textBrowser.toPlainText().splitlines()
        if len(lines) > 16:
            # 只保留最后18行消息
            self.textBrowser.setPlainText('\n'.join(lines[-16:]))  # 更新文本浏览器内容
            self.textBrowser.moveCursor(QtGui.QTextCursor.End)  # 移动光标到文本末尾，以显示最新消息

    def start_video_stream(self):
        if not self.video_thread.isRunning():
            self.video_thread.start_stream()

    def update_image(self, q_image):
        """更新幕布"""
        self.label.setPixmap(QtGui.QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        """全局退出"""
        self.socket_thread.stop_connection()
        self.video_thread.stop_stream()
        if self.matcher_thread:
            self.matcher_thread.stop()
        event.accept()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = Ui_MainWindow()  # 创建主窗口
    main_window.MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())
