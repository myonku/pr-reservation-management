<template>
    <el-descriptions title="个人信息" border>
        <el-descriptions-item :rowspan="2" :width="140" label="头像" align="center">
            <el-image style="width: 100px; height: 100px" :src="`http://127.0.0.1:8000${avatar}`" />
        </el-descriptions-item>
        <el-descriptions-item label="用户名">{{ username }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ phone }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ date_joined }}</el-descriptions-item>
        <el-descriptions-item label="用户等级">
            <template v-if="if_staff === true">
                <el-tag size="small" type="danger">后台员工</el-tag>
            </template>
            <template v-else-if="common_staff === true">
                <el-tag size="small" type="success">普通员工</el-tag>
            </template>
            <template v-else>
                <el-tag size="small">标准</el-tag>
            </template>
        </el-descriptions-item>
        <el-descriptions-item label="个人邮箱" align="center">
            {{email}}
        </el-descriptions-item>

    </el-descriptions>
    <br>
    <el-row :gutter="20">
        <el-col :span="8" :offset="3">
            <div style="padding-top: 5px;text-align: center;">上次登录于：{{ last_login }}</div>
        </el-col>
        <el-col :span="4" :offset="3">
            <el-button type="primary" plain @click="dialogFormVisible=true">修改基本信息</el-button>
            <el-dialog v-model="dialogFormVisible" title="信息更新" width="80%" :close-on-click-modal="false">
                <h4 style="text-align: center;">暂时只支持用户名与用户头像的直接变更，而绑定信息如手机号、邮箱等请前往其他选项进行变更</h4>
                <el-form :model="form">
                    <el-form-item label="用户名" :label-width="60">
                        <el-input v-model="form.username" autocomplete="off" />
                    </el-form-item>
                    <el-form-item label="头像" :label-width="60">
                        <div style="text-align: center;width: 100%;">
                            <el-upload class="upload-demo" drag action="#" darg :before-upload="beforeUpload"
                                :file-list="fileList" :limit="1" :on-change="handleAvatarChange"
                                :on-remove="handleRemove" :on-exceed="handleExceed"
                                :auto-upload="false">
                                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                                <div class="el-upload__text">
                                    拖动文件至此处 或<em> 点击上传</em>
                                </div>
                                <template #tip>
                                    <div class="el-upload__tip">
                                        jpg/png 格式文件且大小不超过 500kb
                                    </div>
                                </template>
                            </el-upload>
                        </div>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <div class="dialog-footer">
                        <el-button @click="dialogFormVisible = false">取消</el-button>
                        <el-button type="primary" @click="submitForm">
                            确认修改
                        </el-button>
                    </div>
                </template>
            </el-dialog>
        </el-col>
        <el-col :span="2">
            <el-button type="success" plain @click="updateUserDetails">刷新数据</el-button>
        </el-col>
    </el-row>
    <br>
    <el-descriptions border>
        <el-descriptions-item label="面部识别码" align="center">
            <el-tag v-if="identity_code" size="small" type="success">生效中</el-tag>
            <el-tag v-else="identity_code" size="small" type="danger">未生效</el-tag>
        </el-descriptions-item>
        <el-descriptions-item align='center'>
            <el-button type="danger" plain @click="dialogCCVisible=true"
                :disabled="!identity_code">注销人脸验证</el-button>&nbsp;
            <el-dialog v-model="dialogCCVisible" title="注销面部验证" width="80%" :close-on-click-modal="false">
                <h3>确定注销人脸信息吗？</h3>
                <h4>这会删除所有采集的信息，并关闭人脸验证功能</h4>
                <hr>
                <template #footer>
                    <div class="dialog-footer">
                        <el-button @click="dialogCCVisible = false">取消</el-button>
                        <el-button type="primary" @click="del_identity">
                            确认注销
                        </el-button>
                    </div>
                </template>
            </el-dialog>
            <el-button type="primary" plain @click="to_update">前往更新</el-button>
        </el-descriptions-item>
    </el-descriptions>
    <br>
    <el-descriptions border>
        <el-descriptions-item label="认证二维码" align="center">
            <div style="padding: 20px;" @click="showModal">
                <qrcode-vue :value="qrData" :size="200" />
            </div>
            <!-- 模态框 -->
            <el-dialog v-model="isModalVisible" width="80%">
                <div style="padding: 20px;">
                    <qrcode-vue :value="qrData" :size="500" />
                </div>
                <template #footer>
                    <div class="dialog-footer">
                        <el-button type="primary" @click="isModalVisible = false">
                            关闭
                        </el-button>
                    </div>
                </template>
            </el-dialog>
        </el-descriptions-item>
        <el-descriptions-item align='center'>
            <el-button type="primary" plain @click="fetchQrData">更新</el-button>
        </el-descriptions-item>
    </el-descriptions>
    <div style="height: 70px;" v-loading.fullscreen.lock="fullscreenLoading"></div>
</template>
<style>
.el-descriptions {
    padding: 16px;
    border: 1px solid lightgray;
    border-radius: 6px;
}
</style>
<script setup>
import { ref, onMounted, reactive } from 'vue';
import { ElMessage, ElNotification } from 'element-plus'
import QrcodeVue from 'qrcode.vue'; // 引入二维码组件  
import { useRouter } from 'vue-router';
const emit = defineEmits(); // 定义 emit  
defineExpose({ QrcodeVue });// 注册QRCode组件  

const router = useRouter();
const fullscreenLoading = ref(false)
const qrData = ref("");
const username = ref("");
const avatar = ref("");
const phone = ref("");
const email = ref("");
const date_joined = ref("");
const last_login = ref("");
const common_staff = ref(false);
const if_staff = ref(false);
const isModalVisible = ref(false);
const dialogFormVisible = ref(false)
const dialogCCVisible = ref(false)
const identity_code = ref(false)
const form = reactive({
    username: '',
})
const fileList = ref([[]])
const avatarUrl = ref(null)

const beforeUpload =(file)=> {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    const isLt500k = file.size / 1024 <= 500;

    if (!isJpgOrPng) {
        ElMessage({
            message: '上传头像图片只能是 JPG或 PNG 格式!',
            type: 'error',
            plain: true,
        })
        return;
    }
    if (!isLt500k) {
        ElMessage({
            message: '上传头像图片大小不能超过 500KB!',
            type: 'error',
            plain: true,
        })
        return;
    }
    return isJpgOrPng && isLt500k; // 允许上传的返回值  
}
const handleRemove =(file)=> {
    // 清除头像预览  
    avatarUrl.value = null;
    fileList.value = []; // 清空文件列表  
}
const handleExceed =(files)=> {
    if(files.length > 1){
        ElMessage({
            message: `只能上传单个文件，当前已选择 ${files.length} 个文件`,
            type: 'error',
            plain: true,
        })
        return;
    }
}
const handleAvatarChange =(file)=> {
    // 仅保存最后上传的文件，确保文件列表中只保留一项  
    fileList.value = [file.raw]; // 直接设置  
    const reader = new FileReader();
    reader.onload = (e) => {
        avatarUrl.value = e.target.result; // 保存预览图 URL  
    };
    reader.readAsDataURL(file.raw);
}  
const submitForm = async()=> {
    dialogFormVisible.value = false;
    const formData = new FormData();
    const token = sessionStorage.getItem('token'); // 从sessionStorage中获取token  
    formData.append('username', form.username);
    formData.append('token', token);
    if (fileList.value.length > 0) {
        formData.append('profile', this.fileList[0]); // 发送第一个文件（头像）  
    }

    // 发送请求到 Django 后端  
    try {
        const response = await this.$http.post('/api/users/update/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        this.$message.success('用户信息已更新!');
    } catch (error) {
        this.$message.error('更新用户信息失败！');
    }
}
const fetchQrData = async () => {
    fullscreenLoading.value = true; // 显示加载状态  
    const token = sessionStorage.getItem('token'); // 从sessionStorage中获取token  
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/update_qrcode`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),  // 发送 token  
        });

        if (!response.ok) {
            throw new Error('网络错误');
        }

        const data = await response.json();
        qrData.value = data.qr_data || '';
        fullscreenLoading.value = false; 
        ElNotification({
            title: '系统消息',
            message: '二维码更新成功！',
            type: 'success',
            position: 'bottom-right',
        })
    } catch (error) {
        fullscreenLoading.value = false; 
        console.error("获取二维码数据失败:", error);
        ElNotification({
            title: '系统消息',
            message: '获取二维码数据失败！',
            type: 'error',
            position: 'bottom-right',
        })
    }
}
const showModal = () => {
    isModalVisible.value = true; // 打开模态框  
};
const updateUserDetails = async () => {
    try{
        fullscreenLoading.value = true; 
        getUserDetails();
        fullscreenLoading.value = false; 
        ElNotification({
            title: '系统消息',
            message: '信息刷新成功！',
            type: 'success',
            position: 'bottom-right',
        })
    } catch {
        fullscreenLoading.value = false; 
        ElNotification({
            title: '系统消息',
            message: '信息刷新失败！',
            type: 'error',
            position: 'bottom-right',
        })
    }
}
const del_identity = async() => {
    dialogCCVisible.value = false;
    fullscreenLoading.value = true; 
    const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    if (!token) {
        console.error("Token is required.");
        fullscreenLoading.value = false; 
        ElMessage({
            message: '验证信息出错，请刷新后尝试',
            type: 'error',
            plain: true,
        })
        return;
    }
    try{
        const response = await fetch('http://127.0.0.1:8000/api/del_identity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),  // 发送 token  
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error fetching user details:", errorData.error);
            fullscreenLoading.value = false; 
            ElNotification({
                title: '系统消息',
                message: '操作失败，与服务器的连接不稳定',
                type: 'error',
                position: 'bottom-right',
            })
            return;
        }
        const data = await response.json();
        const type = (data.code === 1) ? "success" : "error";
        const msg = data.msg;
        ElNotification({
            title: '系统消息',
            message: msg,
            type: type,
            position: 'bottom-right',
        })
    }catch{
        fullscreenLoading.value = false; 
        ElMessage({
            message: '验证信息出错，请刷新后尝试',
            type: 'error',
            plain: true,
        })
    }finally{
        fullscreenLoading.value = false; 
    }
}
// 获取用户信息的函数  
const getUserDetails = async () => {
    const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    if (!token) {
        console.error("Token is required.");
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:8000/api/get_user_detail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),  // 发送 token  
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error fetching user details:", errorData.error);
            return;
        }

        const data = await response.json();
        // 更新状态  
        username.value = data.username || "未绑定"; // 处理空值情况  
        form.username = username.value;
        avatar.value = data.avatar || ""; // 处理空值情况  
        phone.value = data.phone || "未绑定"; // 处理空值情况  
        email.value = data.email || "未绑定"; // 处理空值情况  
        date_joined.value = data.date_joined || "未知"; // 处理空值情况  
        last_login.value = data.last_login || "未知"; // 处理空值情况  
        common_staff.value = data.common_staff || false; // 处理空值情况  
        if_staff.value = data.if_staff || false; // 处理空值情况  
        qrData.value = data.qr_data || '';
        identity_code.value = data.identity_code;
        emit('update:info', {update: 1});
    } catch (error) {
        console.error("Error:", error);
    }
}
const to_update = () => {
    router.push({ name: 'others' });
};
// 在组件挂载时获取用户信息  
onMounted(() => {
    getUserDetails();
    router.replace({ name: 'user' }); // 用 replace 方法以移除该查询参数  
});
</script>
