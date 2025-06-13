<template>

    <div class="alert-con">
        <el-alert v-for="(alert, index) in alerts" :key="index" :title="alert.title" :type="alert.type"
            :description="alert.description" show-icon :data-type="alert.customIdentifier" @close="confirm_msg(alert.customIdentifier)"/>
    </div>

    <div class="sform">
        <h2 class="sform_item fh">欢迎使用XXXX预约系统</h2>
        <div class="sform_item">可以在此处提交你的预约申请，或查询相关的信息。</div>
        <div class="sform_item">具体的时间安排会由内部员工决定，信息可能会随时变更，但一旦提交了预约申请，该申请就会生效并由管理人员进行审核。</div>
        <br>
        <div class="sform_item">
            已经提交的申请不受后续时间安排改动的影响。您无法在同一个起始时刻重复提交申请，但可以在重复的时间段内拥有可用的预约。
            例如可以同时申请10：00-12：00和11：00-13：00的预约。但是在重叠的时间段（11：00-12：00）中通过验证的话，这两个预约申请都将被标记为完成。
        </div>
    </div>

    <div class="sform">
        <h3 class="sform_item fh">接下来一周的可预约情况<span style="font-weight: normal;font-size: medium;">
                <el-popover placement="bottom" title="数据展示" :width="200" trigger="hover"
                    content="具体的可预约小时段不会在此展示，而将在预约申请的数据填写中列出。">
                    <template #reference>
                        <el-icon>
                            <QuestionFilled />
                        </el-icon>
                    </template>
                </el-popover></span></h3>
        <el-table stripe :data="tableData" class="sform_item">

            <el-table-column prop="date" label="日期" width="auto" />
            <el-table-column prop="week" label="星期制" width="auto" />
            <el-table-column prop="valid" label="可预约" width="auto" />
            <el-table-column prop="limit" label="全局数量限制" width="auto" />
            <el-table-column prop="per_limit" label="个人数量限制" width="auto" />
            <el-table-column prop="interval" label="间隔" width="auto" />
        </el-table>
    </div>
    <el-row style="margin-bottom: 35px;">
        <el-col :span="24">
            <div style="text-align: right;width: 100%;">
                <el-button type="primary" plain @click="update_base_dateinfo">刷新基本信息</el-button>
            </div>
        </el-col>
    </el-row>

    <div class="sform">
        <h3 class="sform_item fh">填写新的预约申请</h3>
        <el-form :model="form" :rules="rules" label-width="auto" class="sform_item" ref="ruleFormRef" status-icon>
            <el-form-item label="用户">
                <el-input v-model="form.name" disabled />
            </el-form-item>
            <el-form-item label="目标日期" prop="date">
                <el-select v-model="form.date" placeholder="选择将要通行的日期">
                    <el-option v-for="item in date_list" :key="item.value" :label="item.label" :value="item.value"
                        :disabled="item.disabled" />
                </el-select>
            </el-form-item>
            <el-form-item label="目标时间段">
                <el-col :span="11">
                    <el-form-item prop="timestart">
                        <el-select v-model="form.timestart" placeholder="起始时刻">
                            <el-option v-for="item in hour_list" :key="item.value" :label="item.label"
                                :value="item.value" :disabled="item.disabled" />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="2" class="text-center">
                    <span class="text-gray-500">-</span>
                </el-col>
                <el-col :span="11">
                    <el-form-item>
                        <el-select v-model="form.timeend" placeholder="结束时刻" disabled>
                            <el-option :label="form.timeend" :value="form.timeend" />
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-form-item>
            <el-form-item label="通道" prop="device">
                <el-col :span="16">
                    <el-select v-model="form.device" placeholder="选择将要通过的入口">
                        <el-option v-for="item in device_list" :key="item.value" :label="item.label" :value="item.value"
                            :disabled="item.disabled" />
                    </el-select>
                </el-col>
                <el-col :span="8">
                    <div style="width: 100%;text-align: right;">
                        <el-button type="success" @click="update_base_info">刷新全部数据</el-button>
                    </div>
                </el-col>
            </el-form-item>
            <el-form-item label="邀请人">
                <el-col :span="16">
                    <el-input v-model="form.inviter" disabled placeholder="未检测到邀请信息" />
                </el-col>
                <el-col :span="6">
                    <div style="width: 100%;text-align: right;">使用邀请信息</div>
                </el-col>
                <el-col :span="2">
                    <div style="width: 100%;text-align: right;">
                        <el-switch v-model="form.add_inviter"></el-switch>
                    </div>
                </el-col>
            </el-form-item>
            <el-form-item label="备注" prop="desc">
                <el-input v-model="form.desc" type="textarea" />
            </el-form-item>
            <el-form-item>
                <div style="text-align: right; width: 100%;">
                    <el-button @click="resetForm(ruleFormRef)">重置</el-button>
                    <el-button type="primary" @click="validateForm(ruleFormRef)">提交</el-button>
                </div>
            </el-form-item>
        </el-form>
    </div>
    <div style="height: 60px;" v-loading.fullscreen.lock="fullscreenLoading"></div>
</template>

<script lang="ts" setup>
import axios from 'axios';
import { ElMessage, ElNotification, type FormInstance, type FormRules } from 'element-plus';
import { reactive, ref, onMounted, watch, nextTick, onBeforeUnmount} from 'vue'

const fullscreenLoading = ref(false)
// do not use same name with ref
const device_list = ref([{ value: '无数据', label: '无数据',disabled: true, }])
const date_list = ref([{ value: '无数据', label: '无数据', disabled: true, }])
const hour_list = ref([{ value: '无数据', label: '无数据', disabled: true, }])
const alerts = ref([
    { title: '系统消息', type: 'info', description: '未来几天的预留预约计划发生了变更。请前往预约申请部分查看详情。', customIdentifier: 0 }
    // 其他初始消息  
])
const emit = defineEmits(["msgevent"])
const tableData = ref([
    {
        date: '未知',
        week: '未知',
        valid: '未知',
        limit: '未知',
        per_limit: '未知',
        interval: '0'
    },
])
const socket = ref()
const interval = ref(0)
interface RuleForm {
    name: string
    date: string | null;
    timestart: string | null;
    timeend: string | null;
    inviter: string | null
    add_inviter: boolean
    device: string | null;
    desc: string
}
const ruleFormRef = ref<FormInstance>()
const form = reactive<RuleForm>({
    name: '',
    date: null,
    timestart: null,
    timeend: null,
    inviter: null,
    add_inviter: true,
    device: null,
    desc: '',
})
const addAlert = (title: string, type: string, description: string, customIdentifier:number)=>{
    const newAlert = {
        title: title,
        type: type,
        description: description,
        customIdentifier: customIdentifier
    }
    alerts.value.push(newAlert); // 新增通知  
}
const removeAlert =()=> {
    alerts.value.pop() // 删除最后一个通知  
}

onMounted(() => {
    fetchBaseDateInfo();
    get_all_valid_date();
    get_all_dev();
    getUserInfo();
    removeAlert();
    emit("msgevent", 10);
});

const confirm_msg = async (typex: any) => {
    emit("msgevent", typex)
}

const updatemessage = (msg : any)=>{
    const type = msg.type;
    if (type == 11) {
        const result = msg.result;
        const item1 = result[0];
        const item2 = result[1];
        const item3 = result[2];
        const item4 = result[3];
        const item5 = result[4];
        const item6 = result[5];
        if (item1 !== 0) {
            addAlert("预约通过", "success","你的预约申请已经被审核通过。请前往相关申请部分查看详情。",1)
        }
        if (item2 !== 0) {
            addAlert("预约未通过", "error", "你的预约申请已经被审核拒绝。请前往相关申请部分查看详情。",1)
        }
        if (item3 !== 0) {
            addAlert("预约过期", "info", "你的预约申请已经过期。请前往相关申请部分查看详情。",1)
        }
        if (item4 !== 0) {
            addAlert("系统通知", "info", "未来几天的预留预约计划发生了变更。请前往预约申请部分查看详情。",3)
        }
        if (item5 !== 0) {
            addAlert("预约生效中", "warning", "你的预约申请已生效，请在预定时间内通过。可前往预约申请部分查看详情。",2)
        }
        if (item6 !== 0) {
            addAlert("预约已失效", "error", "你未在限定时间内通过，相关预约已失效。请前往预约申请部分查看详情。",2)
        }

    } else if (type == 12) {

    } else if (type == 13) {

    }
}
defineExpose({
    updatemessage
})
const rules = reactive<FormRules<RuleForm>>(
    {
        date: [{ required: true, message: '请选择目标日期', trigger: 'change' }],
        timestart: [{ required: true, message: '请选择起始时刻', trigger: 'change' }],
        device: [{ required: true, message: '请选择通道', trigger: 'change' }],
        desc: [{ required: true, message: '请输入备注', trigger: 'blur' }],
    }
)

const validateForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            submitForm()
        } else {
            console.log('error submit!', fields)
        }
    })
}
const submitForm = async () => {
    try {
        //await validateForm(formEl); // 等待表单验证完成  
        fullscreenLoading.value = true; // 显示加载状态  
        const response = await axios.post('http://127.0.0.1:8000/api/resvation_submit', form); // 使用 await 等待响应  
        // 检查后端返回的响应数据  
        const { state, success, error } = response.data; // 假设后端返回的数据结构包含这几个字段  
        fullscreenLoading.value = false; // 隐藏加载状态  
        if (state === 0) {
            ElNotification({
                title: '系统消息',
                message: success || "申请提交成功!",
                type: 'success',
                position: 'bottom-right',
            });
        } else {
            ElNotification({
                title: '系统消息',
                message: error || "申请提交失败！",
                type: 'error',
                position: 'bottom-right',
            });
        }

    } catch (error) {
        fullscreenLoading.value = false; // 隐藏加载状态  
        console.error('Submission error:', error);

        ElNotification({
            title: '系统消息',
            message: "申请提交失败！请检查网络或后端服务。",
            type: 'error',
            position: 'bottom-right',
        });
    }
    resetForm(ruleFormRef.value)
}

const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields();
    form.timeend = null;
}


const update_base_info = async () =>{
    try {
        fullscreenLoading.value = true; // 显示加载状态
        resetForm(ruleFormRef.value)
        getUserInfo();
        get_all_valid_date();
        get_all_dev();
        fullscreenLoading.value = false;
        ElMessage({
            message: '数据刷新成功',
            type: 'success',
            plain: true,
        })
    } catch {
        fullscreenLoading.value = false; // 显示加载状态
        ElMessage({
            message: '数据刷新失败',
            type: 'error',
            plain: true,
        })
    }
}
const update_base_dateinfo = () => {
    try{
        fullscreenLoading.value = true; // 显示加载状态
        fetchBaseDateInfo();
        fullscreenLoading.value = false; 
        ElMessage({
            message: '数据刷新成功',
            type: 'success',
            plain: true,
        })
    } catch {
        fullscreenLoading.value = false; 
        ElMessage({
            message: '数据刷新失败',
            type: 'error',
            plain: true,
        })
    }
}
const fetchBaseDateInfo = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/get_base_date_info');  
        const data = response.data;
        tableData.value = data.map((item: { date: string; valid: boolean; limit: number; interval: number; }) => {
            const dateObj = new Date(item.date);
            const weekDays = ['日', '一', '二', '三', '四', '五', '六'];
            const week = '星期' +  weekDays[dateObj.getUTCDay()]; // 获取星期几  

            const valid = item.valid ? '是' : '否'; // 根据 if_valid 转换  
            const limit = item.limit > 10000 ? '无限制' : `${item.limit}条`;
            const per_limit = item.limit > 10000 ? '无限制' : `${item.limit / 10}条`;
            const interval = `${item.interval}小时`; // 转换间隔  

            return {
                date: item.date, // 原始日期  
                week, // 星期  
                valid, // 可预约  
                limit, // 最大预约人数  
                per_limit, // 每人预约人数  
                interval, // 预约间隔  
            };
        });
    } catch (error) {
        console.error('获取数据失败:', error);
    }
}
const get_all_dev = async () => {
    try {
        const response = await axios.post(`http://127.0.0.1:8000/api/get_all_dev`, { "key": 1 });
        if (response.data.list && Array.isArray(response.data.list)) {
            const deviceList = response.data.list.map((name: any) => ({
                value: name,  // value 字段  
                label: name   // label 字段  
            }));
            
            // 假设 device_list 是您存储下拉选项的变量  
            device_list.value = deviceList;  
        } else {
            console.error("无效的数据格式：", response.data);
        }

    } catch (error) {
        console.error('获取数据失败:', error);
    }
}
const get_all_valid_date = async () => {
    try {
        const response = await axios.post(`http://127.0.0.1:8000/api/get_all_valid_date`, { "key": 1 });
        if (response.data.list && Array.isArray(response.data.list)) {
            const dataList = response.data.list.map((name: any) => ({
                value: name,  // value 字段  
                label: name   // label 字段  
            }));

            // 假设 device_list 是您存储下拉选项的变量  
            date_list.value = dataList;
        } else {
            console.error("无效的数据格式：", response.data);
        }

    } catch (error) {
        console.error('获取数据失败:', error);
    }
}
const getUserInfo = async () => {
    const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    if (!token) {
        console.error("Token is required.");
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:8000/api/get_user_info', {
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
        form.name = data.username || "未知"; // 处理空值情况  
    } catch (error) {
        console.error("Error:", error);
    }
};

// 监听 date 的变化  
watch(() => form.date, async (newDate) => {
    if (newDate) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/get_date_hours', { date: newDate });
            const hours = response.data.hours;
            form.timestart = null;
            form.timeend = null;
            // 更新 hour_list  
            hour_list.value = hours.map((hour: any) => ({
                value: hour,
                label: hour,
                disabled: false // 根据需要设置是否禁用  
            }));
            interval.value = response.data.interval;
        } catch (error) {
            console.error('获取可预约时刻失败:', error);
            ElMessage.error('获取可预约时刻失败');
        }
    }else{
        hour_list.value = [{ value: '无数据', label: '无数据', disabled: true, }]
    }
})
watch(() => form.timestart, async (newTime) =>{
    // 如果 timestart 有值，更新 timeend  
    if (newTime) {
        form.timeend = null;
        const startHour = parseInt(newTime.split(':')[0]); // 获取小时部分  
        const endHour = startHour + interval.value - 1; // 计算结束小时  
        form.timeend = `${endHour}:59`; // 设置 timeend，确保不超过 23:00  
    }
})
onBeforeUnmount(() => {
    //disconnect()
})

</script>

<style>
.fh{
    padding-bottom: 20px;
    border-bottom: 1px solid lightgray;
    font-weight: normal;
}
.sform{
    text-align: center;
    padding-left: 10%;
    padding-top: 10px;
    padding-bottom: 20px;
    border: 1px solid lightgray;
    border-radius: 6px;
    margin-bottom: 40px;
}

.sform_item{
    max-width: 86% !important;
}
.el-alert {
    margin-bottom: 20px !important;
}
.alert-con{
    margin: 10px 0px 30px 0px;
}
.el-alert:first-child {
    margin: 0;
}

</style>