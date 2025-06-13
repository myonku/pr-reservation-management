
#从前端传来的帧中进行处理，此处只需要获取特征向量，不用特地装torch环境干这事儿

import base64
import cv2
import face_recognition
import numpy as np
import torch
import threading
from queue import Queue


""" python setup.py build_ext --inplace """

def clean_base64_string(base64_string):
    if base64_string.startswith("data:image/png;base64,"):
        base64_string = base64_string.replace("data:image/png;base64,", "")
    return base64_string.strip()


def pad_base64_string(base64_string):
    # Base64 字符串需要有 4 的倍数长度
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += "=" * (4 - missing_padding)
    return base64_string


# 启动多线程处理
def manage_frames(frames):
    """提取人脸特征向量并返回特征向量均值"""
    feature_vectors = []
    lock = threading.Lock()
    frame_queue = Queue()

    # 处理特征向量的线程数
    NUM_THREADS = 4
    exit_flag = False
    def process_faces():
        while not exit_flag:
            if not frame_queue.empty():
                # 从队列中获取一帧图像
                try:
                    frame_data = frame_queue.get()
                    # 解码 Base64 编码的图像数据
                    cleaned_frame_data = clean_base64_string(frame_data)
                    img_data = base64.b64decode(pad_base64_string(cleaned_frame_data))
                    np_array = np.frombuffer(img_data, np.uint8)  # 转换为 NumPy 数组
                    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # 解码为 OpenCV 图像格式
                    # 将 BGR 转为 RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 查找当前帧中的人脸
                    face_locations = face_recognition.face_locations(rgb_frame)
                except:
                    face_locations = None

                # 检查是否发现任何人脸
                if face_locations:
                    face_encodings = face_recognition.face_encodings(
                        rgb_frame, face_locations, num_jitters=1
                    )
                    with lock:
                        feature_vectors.extend(face_encodings)  # 将特征向量添加到列表
                else:
                    continue
                # 处理完该帧
                frame_queue.task_done()  # 标记该帧已处理完成

    def get_average_vec(feature_vectors):
        if feature_vectors:  # 确保特征向量列表非空
            tensor_vectors = np.array(feature_vectors)  # 转换为 NumPy 数组
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            tensor_vectors = torch.tensor(tensor_vectors, device=device)
            # 计算均值和标准差
            mean = torch.mean(tensor_vectors, dim=0)
            std = torch.std(tensor_vectors, dim=0)
            """ # 创建一个新的图表窗口
            plt.figure()  
            # 绘制均值
            plt.plot(mean.cpu().numpy(), label='Mean', color='blue', marker='o')  
            # 绘制标准差
            plt.plot(std.cpu().numpy(), label='Standard Deviation', color='red', marker='x')  

            # 添加图表标题和标签
            plt.title('Mean and Standard Deviation of Feature Vectors')  
            plt.xlabel('Feature Index')  
            plt.ylabel('Value')  
            plt.xticks(range(len(mean)))  # 适应特征索引  

            # 添加图例
            plt.legend()  

            plt.show(block=False)  # 防止阻塞  
            plt.pause(0.001)       # 给 GUI 系统时间来更新  
            plt.show()    """
            # 设置阈值，此处为x倍标准差
            threshold = 2.25
            filtered_vectors = tensor_vectors[
                torch.all(torch.abs(tensor_vectors - mean) <= threshold * std, dim=1)
            ]
            print("通过的样本数：" + str(len(filtered_vectors)))
            # 计算新的均值（排除偏差过大的特征向量）
            if filtered_vectors.size(0) >= 10:  # 确保过滤后数据量足够
                final_average_encoding = torch.mean(filtered_vectors, dim=0)
            else:
                final_average_encoding = None
            return final_average_encoding
        else:
            return None


    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=process_faces)
        thread.daemon = True
        thread.start()
    for frame in frames:  # `frames` 是从前端传入的包含 Base64 编码的图像字符串列表
        frame_queue.put(frame)
    frame_queue.join()  # 等待队列中的所有任务完成
    # 设置退出标志
    exit_flag = True
    # 计算最终的平均特征向量
    return get_average_vec(feature_vectors)
