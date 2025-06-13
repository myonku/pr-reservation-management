import json

from PyQt5 import QtCore
from websocket import create_connection, WebSocketException


class SocketThread(QtCore.QThread):
    message_received = QtCore.pyqtSignal(str)  # 定义信号用于发送消息到主线程

    def __init__(self, url='127.0.0.1'):
        super().__init__()
        self.url = "ws://" + url + ":8000/ws/clientsocket/"
        self.ws = None
        self.running = False
        self.device = "测试1"

    def update_url(self, new_url):
        """更新URL"""
        self.url = "ws://" + new_url + ":8000/ws/clientsocket/"

    def run(self):
        self.message_received.emit("正在尝试连接到服务器。")
        try:
            self.ws = create_connection(self.url)  # 建立 WebSocket 连接
            self.ws.connect(self.url)
            self.running = True
            self.message_received.emit("已连接到服务器。")
            self.send_message({"type": 10, "data": "建立连接::来自设备[{}]的请求".format(self.device)})
            result = ""
            while self.running:
                # 等待接收消息
                try:
                    data = self.ws.recv()  # 接收数据，大小可以根据需要调整
                except WebSocketException as e:
                    data = None
                    self.message_received.emit("发生错误，接收服务器通信失败。")  # 发射信号到主线程

                if data:
                    if type(data) == bytes:
                        message = data.decode('utf-8')  # 解码为字符串
                    else:
                        message = data
                    result += message
                    if result.endswith('end'):
                        self.message_received.emit(result.rstrip("end"))  # 发射信号到主线程
                        result = ""
        except Exception as e:
            self.message_received.emit(f"连接或数据错误: {str(e)}")
            self.running = False
            self.stop()
        finally:
            self.send_message({"type": 10, "data": "连接断开::设备[{}]已经下线".format(self.device)})
            if self.ws:
                self.ws.close()  # 确保关闭 WebSocket 连接
            self.stop()


    def send_message(self, message):
        """主动发送消息到服务器"""
        try:
            message = json.dumps(message)
        except json.JSONDecodeError:
            message = message
        if self.ws and self.running:
            try:
                self.ws.send(message)  # 发送字符串消息
            except Exception as e:
                self.message_received.emit(f"数据发送失败: {str(e)}")
        else:
            self.message_received.emit("未连接到服务器，无法发送消息。")

    def start_connection(self):
        """启动连接"""
        self.start()
        self.running = True


    def stop_connection(self):
        """停止连接"""
        self.send_message({"type": 10, "data": "连接断开::设备[{}]已经下线".format(self.device)})
        self.stop()
        self.running = False


    def stop(self):
        """停止线程并关闭 socket"""
        if self.running:
            self.running = False
            if self.ws:
                self.ws.close()
                self.ws = None
                self.message_received.emit("已关闭与服务器的连接。")
        else:
            self.message_received.emit("未处于连接状态。")
