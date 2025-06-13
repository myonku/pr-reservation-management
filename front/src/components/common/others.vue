<template>
    <div class="main_con">
        <h3>更新电话或邮箱绑定信息</h3>
    </div>
    <div class="main_con">
        <h3>更新您的面部识别信息</h3>
        <div style="text-align: center;">
            此处不会收集或存储任何图像数据，只需要在实时的视频流中采集您的面部特征并生成对应的特征码。
        </div>
        <div style="text-align: center;">
            为了确保数据的采集精度，请在光线明亮处进行更新。
        </div><br>
        <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="点击此处开始信息采集" name="1">
                <div class="vid">
                    <video width="480" height="480" ref="video" autoplay playsinline style="object-fit:cover"></video>
                    <canvas width="480" height="480" ref="canvasx"></canvas>
                </div>
                <div style="width: 100%;text-align: center;">
                    检测开始后，请保持面部位于屏幕中央（视频流会实时显示在上方的区域），等待检测进程完成。
                </div>
                <div style="width: 100%;text-align: center;border-bottom: 1px solid lightgray;padding-bottom: 10px">
                    为确保更准确的数据采集，请面向相机设备，保持端正姿态约五秒以获得可靠的识别信息。
                </div>
                <br>
                <el-progress v-if="if_video" :percentage="cap_process" stroke-width="15" :status="cap_status" striped
                    striped-flow />
                <br>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-button @click="stopVideoStream" type="danger" :disabled="!if_video">终止认证</el-button>
                    </el-col>

                    <el-col :span="12">
                        <el-button type="primary" @click="startVideoStream">开始认证</el-button>
                    </el-col>
                </el-row>

                <p v-if="message">{{ message }}</p>
                <div v-if="faceDetected">
                    <p>正在检测中...</p>
                </div>
            </el-collapse-item>
        </el-collapse>
    </div>

    <div class="main_con">
        <h3>相关的预约申请信息</h3>
        <el-row>
            <el-col :span="12"></el-col>
            <el-col :span="8" style="text-align: right;">
                <el-radio-group v-model="radio">
                    <el-radio-button :value="'2'">提交时间</el-radio-button>
                    <el-radio-button :value="'1'">目标时间</el-radio-button>
                </el-radio-group>
            </el-col>
            <el-col :span="4" style="text-align: right;">&nbsp;倒序&nbsp;<el-switch v-model="value1" /></el-col>

        </el-row>
        <br>
        <el-table :data="tableData" stripe height="280" style="width: 100%">
            <el-table-column type="expand">
                <template #default="props">
                    <div m="4">
                        <p m="t-0 b-2">通道: {{ props.row.device.name }}</p>
                        <p m="t-0 b-2">时间段: {{ props.row.res_start_time.slice(-5) + "--" +
                            props.row.res_dec_time.slice(-5) }}</p>
                        <p m="t-0 b-2">审核时间: {{ props.row.audit_time || "未审核" }}</p>
                        <p m="t-0 b-2">邀请人: {{ props.row.inviter || "无" }}</p>
                        <p m="t-0 b-2">描述: {{ props.row.description }}</p>
                        <p v-if="props.row.apd_ori_resvation.length > 0" m="t-0 b-2">
                            通过状态: {{ props.row.apd_ori_resvation[0].state_apd }}
                        </p>
                        <p v-if="props.row.apd_ori_resvation.length > 0" m="t-0 b-2">
                            通过时间: {{ props.row.apd_ori_resvation[0].completed_time || "未通过"}}
                        </p>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="提交时间" prop="res_time" />
            <el-table-column label="目标时间（开始）" prop="res_start_time" />
            <el-table-column label="结果" prop="state" />
        </el-table>
        <br>
        <el-pagination background 
            :page-size="10" 
            :pager-count="5" 
            layout="prev, pager, next" 
            :page-count="pagecount"
            @current-change="handlePageChange" />
    </div>
    <div style="height: 60px;" v-loading.fullscreen.lock="fullscreenLoading"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import * as faceapi from 'face-api.js';
import { ElNotification } from 'element-plus';
import axios from 'axios';
const video = ref();
const videoStream = ref(null);
const message = ref('');
const faceDetected = ref(false);
const frames = ref([]);
const framesCount = ref(25); //总共产生的帧数  
const cap_process = ref(0)
const cap_status = ref('exception')
let detectionInterval = null; // 定义定时器变量
const if_video = ref(false)
const fullscreenLoading = ref(false)
const canvasx = ref()
//
const value1 = ref(true)   //倒序
const radio = ref("2")    //排序依据
const pagekey = ref("2")
const pagecount = ref(1)
const pagenum = ref(1)


const tableData = ref([
    {
        res_time: '1999-01-01',
        res_start_time: '1999-01-01',
        res_end_time: "1999-01-01",
        res_dec_time: '1999-01-01',
        inviter: '',
        state: '未知',
        audit_time: null,
        device: {"name":'未知'},
        description: '未知',
        apd_ori_resvation: [{
            "state_apd": "未知",
            "completed_time":"未知"
        }]
    },
])
// 监听 value1 和 radio 的变化  
watch([value1, radio], () => {
    //pagenum.value = 1; // 将页码重置为1（可选）  
    get_self_records(); // 调用请求函数  
});
onMounted(async () => {
    load_models();
    get_self_records();
})
onBeforeUnmount(() => {
    stopFaceDetection();
})
const handlePageChange = (newPage) => {
    pagenum.value = newPage; // 更新当前页码  
    get_self_records(); // 重新获取数据  
};
const get_self_records = async () => {
    const token = sessionStorage.getItem('token'); // 从sessionStorage中获取token  
    if (!token) {
        console.error("Token is required.");
        return;
    }
    let params = new URLSearchParams();
    params.append("key", pagekey.value);
    params.append("page_num", pagenum.value);
    params.append("sortBy", radio.value);
    params.append("isDescending", value1.value);
    params.append("token", token);
    try {
        const response = await axios.post("http://127.0.0.1:8000/api/v_res_list", params);

        const data = response.data; // 返回 JSON 格式  
        tableData.value = data.page; // 更新结果数据  
        pagenum.value = data.pagenum; // 更新当前页码  
        pagecount.value = data.page_last; // 设置总页数  
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
const load_models = async () => {
    try {
        await Promise.all([
            faceapi.loadTinyFaceDetectorModel(`/models`),
            faceapi.loadFaceLandmarkModel(`/models`),
            //faceapi.nets.faceRecognitionNet.loadFromUri(`/models`),  
        ])
    } catch {
        console.log("加载模型失败")
    }
}
// 开始视频流  
const startVideoStream = async () => {
    ElNotification({
        title: '系统提示',
        message: "采集即将开始，请正对相机设备",
        type: 'info',
        position: 'bottom-right',
    });
    frames.value = [];
    cap_process.value = 0;
    cap_status.value = "excption";
    try {
        const constraints = {
            video: {
                width: { ideal: 480 },  // 请求理想宽度  
                height: { ideal: 480 }, // 请求理想高度  
                facingMode: "user" // 如果希望使用前置摄像头，可以设置为 “user” 或 “environment”  
            }
        };  
        videoStream.value = await navigator.mediaDevices.getUserMedia(constraints);
        if_video.value = true;
        video.value.srcObject = videoStream.value; // 确保实时显示视频流  
        message.value = '视频流已开始';
        video.value.onloadeddata = () => {
            startFaceDetection(); // 视频流加载完成后开始检测人脸
        };
    } catch (error) {
        stopVideoStream();
        stopFaceDetection();
    }
}

// 停止视频流  
const stopVideoStream = () => {
    canvasx.value.getContext('2d')?.clearRect(0, 0, canvasx.value.width, canvasx.value.height);
    if_video.value = false;
    cap_process.value = 0;
    cap_status.value = "exception";
    if (detectionInterval) { clearInterval(detectionInterval) };
    detectionInterval = null;
    faceDetected.value = false; // 如果需要，重置人脸检测状态 
    if (videoStream.value) {
        const tracks = videoStream.value.getTracks();
        tracks.forEach(track => track.stop()); // 停止每一个媒体轨道  
        video.value.srcObject = null; // 清空视频元素的srcObject  
        videoStream.value = null; // 清空videoStream的引用  
        message.value = '检测已停止'; // 给用户反馈   
    }
}
const startFaceDetection = () => {
    detectionInterval = setInterval(detectFace, 300);
}
const stopFaceDetection = () => {
    clearInterval(detectionInterval);
    detectionInterval = null;
}
const detectFace = async () => {         //获取视频帧
    try {
        const detections = await faceapi.detectSingleFace(video.value, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks();
        faceapi.matchDimensions(canvasx.value, { width: canvasx.value.width, height: canvasx.value.height });
        // 清除 Canvas  
        canvasx.value.getContext('2d')?.clearRect(0, 0, canvasx.value.width, canvasx.value.height); 
        
        if (detections) {
            
            const resizedDections = faceapi.resizeResults(detections, { width: canvasx.value.width, height: canvasx.value.height });
            faceDetected.value = true;
            message.value = '';

            faceapi.draw.drawDetections(canvasx.value, resizedDections);
            faceapi.draw.drawFaceLandmarks(canvasx.value, resizedDections);

            if (frames.value.length < framesCount.value) {
                const canvas = document.createElement('canvas');
                canvas.width = video.value.videoWidth;
                canvas.height = video.value.videoHeight;
                const context = canvas.getContext('2d');
                context.drawImage(video.value, 0, 0, canvas.width, canvas.height);
                const frameDataUrl = canvas.toDataURL();
                frames.value.push(frameDataUrl); // 存储视频帧  
                cap_process.value = (frames.value.length / framesCount.value) * 100
                if (cap_process.value < 40) {
                    cap_status.value = 'exception'
                } else if (cap_process.value === 100) {
                    cap_status.value = 'success'
                } else {
                    cap_status.value = 'warning'
                }
            } else {
                sendFrames();
                stopVideoStream();
            }
        } else {
            message.value = '未检测到人脸，请调整您的面部位置';
            faceDetected.value = false;
        }
    } catch {
        stopVideoStream();
    }
}

const sendFrames = async () => {
    fullscreenLoading.value = true; // 显示加载状态
    const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    try {
        const response = await fetch('http://localhost:8000/api/get_frames', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ frames: frames.value, token: token }),
        });

        if (!response.ok) {
            const errorText = await response.text(); // 获取错误响应文本  
            console.error('HTTP 错误:', response.status, errorText);
            fullscreenLoading.value = false;
            return; // 结束函数  
        }

        const result = await response.json();
        handleBackendResponse(result); // 处理后端响应  
    } catch (error) {
        fullscreenLoading.value = false;
        ElNotification({
            title: '系统错误',
            message: "连接失败，请检查用户状态或网络连接",
            type: 'error',
            position: 'bottom-right',
        });
    } finally {
        fullscreenLoading.value = false;
    }
}

const handleBackendResponse = (result) => {
    fullscreenLoading.value = false;
    const code = result.code;
    const content = result.content;
    if (code == 0) {
        ElNotification({
            title: '更新成功',
            message: content,
            type: 'success',
            position: 'bottom-right',
        });
    } else {
        ElNotification({
            title: '操作失败',
            message: content,
            type: 'error',
            position: 'bottom-right',
        });
    }
}  
</script>

<style>
.main_con {
    text-align: center;
    padding-left: 10%;
    padding-right: 10%;
    padding-top: 10px;
    padding-bottom: 20px;
    border: 1px solid lightgray;
    border-radius: 6px;
    margin-bottom: 40px;
}
.el-pagination {
    justify-content: center;
}
.vid {
    position: relative;
    text-align: center;
    margin-bottom: 20px;
    border-radius: 5px;
    height: 480px;
    border: 2px solid lightgray;
}
.el-switch{
    padding-bottom: 4px;
}
.vid video, .vid canvas{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>