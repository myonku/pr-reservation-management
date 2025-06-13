<template>
    <form action="#">
        <div class="row mcr-mein" :id="'mar-manage' + number">
            <div class="col-lg-5 text-start">
                <input type="checkbox" class="btn-check" :id="'checkdate' + number"
                    @change="handleDateUnavailableChange" autocomplete="off" v-model="isDateUnavailable" />
                <label class="btn btn-outline-danger" :for="'checkdate' + number">
                    <span v-if="number != 0">将当日设为不可用</span>
                    <span v-else>将全部日期设为不可用</span>
                </label>
            </div>
            <div style="padding-right:6px" class="col-lg-2 align-middle xmin-mcr text-end">选择预约时段：</div>
            <div class="col-lg-auto text-end btn-group" role="group" aria-label="Basic checkbox toggle button group">
                <input type="radio" class="btn-check" :name="'timeint' + number" :id="'timeint' + number + '-1'"
                    v-model="selectedTime" value="2" autocomplete="off" checked @click="sctime" />
                <label class="btn btn-outline-info" :for="'timeint' + number + '-1'">2小时</label>

                <input type="radio" class="btn-check" :name="'timeint' + number" :id="'timeint' + number + '-2'"
                    v-model="selectedTime" value="3" autocomplete="off" @click="sctime" />
                <label class="btn btn-outline-info" :for="'timeint' + number + '-2'">3小时</label>

                <input type="radio" class="btn-check" :name="'timeint' + number" :id="'timeint' + number + '-3'"
                    v-model="selectedTime" value="4" autocomplete="off" @click="sctime" />
                <label class="btn btn-outline-info" :for="'timeint' + number + '-3'">4小时</label>
            </div>
            <div class="col-lg-2 text-end btn-group" role="group" aria-label="Basic checkbox toggle button group">
                <select class="form-select" :id="'mcr-select' + number" aria-label="Default select example"
                    v-model="maxAppointments" @change="handleMaxAppointmentsChange">
                    <option value="99999998" selected>选择最多预约数</option>
                    <option value="10">最多预约：10</option>
                    <option value="50">最多预约：50</option>
                    <option value="100">最多预约：100</option>
                    <option value="99999999">最多预约：无限制</option>
                </select>
            </div>
        </div><br>
        <div class="btn-group" :id="'mcr-manage' + number" role="group" aria-label="Basic checkbox toggle button group">
            <div v-for="i in 24" :key="i" class="checkbox-wrapper">
                <input type="checkbox" :class="'btn-check btn-' + number" :id="'btncheck' + number + '-' + i"
                    v-model="selectedHours[i - 1]" @change="handleCheckboxChange($event.target, number - 1, i - 1)"
                    :disabled="isDateUnavailable || isHourDisabled(i)" autocomplete="off" />
                <label class="btn"
                    :class="{ 'btn-outline-primary': buttonStates[i - 1] === 'primary', 'btn-warning': buttonStates[i - 1] === 'warning' }"
                    :for="'btncheck' + number + '-' + i">
                    ○ - {{ formatHour(i - 1) }} -&gt;
                </label>
            </div>
        </div>
        <hr>
        <div class="btn-grp-check row">
            <div class="col-lg-3 text-start">
                <button type="button" class="btn btn-warning position-relative"
                    @click="update_default()">设为默认</button>&nbsp;
                <button type="button" class="btn btn-primary position-relative" @click="update_time_data()">刷新</button>
            </div>
            <div class="col-lg-7"></div>
            <div class="col-lg-2 text-end">
                <button type="button" class="btn btn-success position-relative"
                    @click="centerDialogVisible = true">确认修改</button>
            </div>
        </div>

    </form>
    <el-dialog v-model="centerDialogVisible" :title="'更新当日的时间段安排  ' +  this.xdate" width="500" align-center
        :close-on-click-modal="false">
        <span>出于对管理便捷与信息准确的考虑，请尽可能不要频繁变动该部分的信息。</span>
        <div style="text-align: right;padding-right: 20px;"><span> <strong>当日已修改：{{ tr_num }}次</strong></span></div>
        <div style="text-align: right;padding-right: 20px;"><span> 上次更新于：{{ tr_time }}</span></div>
        <br>

        <template #footer>
            <div class="dialog-footer">
                <el-button type="danger" @click="fct()">
                    确认更改
                </el-button>
                <el-button type="primary" @click="centerDialogVisible = false">返回</el-button>
            </div>
        </template>
    </el-dialog>
</template>
<style>
body{
    width: 100% !important;
}
footer{
    padding-bottom: 0 !important;
}
</style>
<script>
import axios from 'axios';
import { ElMessage, ElNotification } from 'element-plus'
import {format} from "date-fns"
export default {
    props: {
        number: {
            type: Number,
            required: true,
            validator: (value) => value >= 0 && value <= 7
        },
    },
    data() {
        return {
            isDateUnavailable: false,  //是否可用
            selectedTime: '2',   //间隔
            maxAppointments: '99999998',  //最大预约
            selectedHours: Array(24).fill(false),
            buttonStates: Array(24).fill('primary'), // 每个按钮的样式状态 
            tr_num: 0,
            centerDialogVisible: false,
            xdate: '',
            tr_time: '',
        };
    },
    watch: {
        //
    }, 
    methods: {
        async get_detail(){
            let params = new URLSearchParams();
            const dateToFetch = this.getDateByNumber(this.number);
            params.append("date", dateToFetch);
            try{    
                const response = await axios.post(`http://127.0.0.1:8000/api/get_date_detail`, params);
                const data = response.data;
                this.tr_num = data.transform_num;
                this.tr_time = data.updated_at;
            }catch{
                console.log("fetch date detail failed")
            }
        },
        async update_default(){
            try { 
                this.fetchAppointmentData(0,0);
                ElMessage({
                    message: '已设置为默认选项数据',
                    type: 'success',
                    plain: true,
                })
            } catch {
                ElMessage({
                    message: '默认值刷新失败',
                    type: 'error',
                    plain: true,
                })
            }
            this.get_detail();
        },
        async fct(){
            this.centerDialogVisible = false;
            this.fetchAppointmentData(1,1);
        },
        async update_time_data() {
            try {
                this.fetchAppointmentData(1,0);
                ElMessage({
                    message: '数据已刷新',
                    type: 'success',
                    plain: true,
                })
            } catch {
                ElMessage({
                    message: '数据刷新失败',
                    type: 'error',
                    plain: true,
                })
            }
            this.get_detail();
        },
        sctime(){
            this.buttonStates.fill('primary');
            this.selectedHours.fill(false); // 取消所有时刻按钮的选中状态  
        },
        handleDateUnavailableChange() {
            // 切换日期不可用状态  
            // 如果设置为不可用，则取消所有时刻的选择  
            if (this.isDateUnavailable) {
                this.selectedHours.fill(false); // 取消所有时刻按钮的选中状态  
                this.buttonStates.fill('primary');
            }
        },

        findClosestCheckedPre(btns, buttonIndex) {
            for (let index = buttonIndex - 1; index >= 0; index--) {
                if (btns[index]) {
                    return index;
                }
            }
            return null;
        },
        findClosestCheckedNxt(btns, buttonIndex) {
            for (let index = buttonIndex + 1; index < btns.length; index++) {
                if (btns[index]) {
                    return index;
                }
            }
            return null;
        },  
        handleCheckboxChange(checkbox, groupIndex, buttonIndex) {
            const buttons = this.selectedHours; // 使用数据状态代替 DOM 查询  
            const i = parseInt(this.selectedTime) || 0; // 将 i 设置为用户选择的时间或0  

            // 定义需要检查的范围  
            const previousStart = Math.max(0, buttonIndex - (i - 1));
            const subsequentEnd = Math.min(buttons.length, buttonIndex + (i - 1));

            // 检查前面和后续的按钮状态  
            const previousButtons = buttons.slice(previousStart, buttonIndex);
            const subsequentButtons = buttons.slice(buttonIndex + 1, subsequentEnd);

            const previousChecked = previousButtons.some((_, idx) => buttons[previousStart + idx]);
            const subsequentChecked = subsequentButtons.some((_, idx) => buttons[buttonIndex + 1 + idx]);

            // 检查按钮被选中  
            if (checkbox.checked) {
                this.buttonStates[buttonIndex] = 'primary'; // 第一个按钮样式切换  
                // 找到后续的最近被选中的按钮  
                const closestCheckedNxt = this.findClosestCheckedNxt(buttons, buttonIndex);

                // 如果后续有被选中的按钮  
                if (closestCheckedNxt) {
                    const closestIndex = closestCheckedNxt;
                    const upperLimit = Math.min(closestIndex, buttonIndex + i);
                    for (let k = buttonIndex + 1; k < upperLimit; k++) {
                        this.buttonStates[k] = 'warning'; // 设置样式为 btn-outline-warning  
                    }
                } else {
                    // 如果没有被选中的按钮，则将后面的 i - 1 个按钮样式设为 btn-outline-warning  
                    for (let k = buttonIndex + 1; k <= Math.min(buttons.length - 1, buttonIndex + (i - 1)); k++) {
                        this.buttonStates[k] = 'warning'; // 设置样式为 btn-outline-warning  
                    }
                }
            } else { // 处理按钮被解除选中  
                // 找到后续的最近被选中的按钮  
                const closestCheckedNxt = this.findClosestCheckedNxt(buttons, buttonIndex);

                // 如果后续有被选中的按钮  
                if (closestCheckedNxt) {
                    const closestIndex = closestCheckedNxt;
                    // 恢复 x 之后到 closestCheckedNxt 之前的按钮样式  
                    for (let k = buttonIndex + 1; k < closestIndex; k++) {
                        this.buttonStates[k] = 'primary'; // 恢复样式  
                    }
                } else {
                    // 如果没有被选中的按钮，则恢复后面 i - 1 个按钮样式  
                    for (let k = buttonIndex + 1; k <= Math.min(buttons.length - 1, buttonIndex + (i - 1)); k++) {
                        this.buttonStates[k] = 'primary'; // 恢复样式  
                    }
                }

                // 检查按钮前面是否有被选中按钮  
                const closestCheckedPre = this.findClosestCheckedPre(buttons, buttonIndex);
                if (closestCheckedPre !== null) {
                    const closestIndex = closestCheckedPre;
                    // 将 closestCheckedPre 之后 i - 1 个按钮样式统一设置为 btn-outline-warning  
                    for (let k = closestIndex + 1; k <= Math.min(buttons.length - 1, closestIndex + (i - 1)); k++) {
                        if (!buttons[k]) {
                            this.buttonStates[k] = 'warning'; // 设置样式为 btn-outline-warning  
                        }
                    }
                }
            }
        },

        
        formatHour(index) {
            const hour = index; // 从0到23  
            return hour < 10 ? '0' + hour + ':00' : hour + ':00'; // 格式化小时  
        },

        isHourDisabled(hour) {
            const selectedHourCount = parseInt(this.selectedTime) || 0;
                // 如果 selectedTime 变化了，先将 selectedHours 设置为非选中  
                for (let i = 0; i < 24; i++) {
                    if (i >= 25 - selectedHourCount) {
                        this.selectedHours[i] = false; // 清除checkbox 状态  
                    }
                }
            return hour > 25 - selectedHourCount; // 禁用  
        },  

        async fetchAppointmentData(dayx = 1, mk = 0) {
            let dateToFetch;
            if (dayx != 1){
                dateToFetch = "1999-01-01";
            }else{
                dateToFetch = this.getDateByNumber(this.number); // 获取对应的日期  
            }
            if (dateToFetch != "1999-01-01"){
                this.xdate = dateToFetch;
            }else{
                this.xdate = "全部日期";
            }
            
            let params = new URLSearchParams();
            params.append("date", dateToFetch);
            if(mk===0){
                try {
                    const response = await axios.post(`http://127.0.0.1:8000/api/get_appointments`, params);
                    this.handleFetchedData(response.data);
                } catch (error) {
                    console.error("Error fetching appointment data:", error);
                }
            }else{
                try {
                    params.append("isDateUnavailable", this.isDateUnavailable);
                    params.append("maxAppointments", this.maxAppointments);
                    params.append("selectedTime", this.selectedTime);
                    params.append("selectedHours", this.selectedHours);

                    const response = await axios.post(`http://127.0.0.1:8000/api/update_appointments`, params);
                    const data = response.data;
                    const status = data.status;
                    const message = data.message;
                    ElNotification({
                        title: "系统消息",
                        type: status,
                        message: message,
                        position: 'bottom-right',
                    })
                } catch (error) {
                    ElNotification({
                        title: "系统消息",
                        type: "error",
                        message: "发生错误，与服务器连接失败!",
                        position: 'bottom-right',
                    })
                }
                
            }
            this.get_detail();
        },
        getDateByNumber(number) {
            if(number != 0){
                const today = new Date();
                today.setDate(today.getDate() + number + 2); // 距今number+2天  
                return format(today, 'yyyy-MM-dd'); // 格式化为 YYYY-MM-DD  
            }
            else{
                return "1999-01-01";
            }
            
        },
        
        handleFetchedData(data) {
            this.isDateUnavailable = !data.if_valid;
            if (this.isDateUnavailable === true){
                return;
            };
            this.selectedTime = data.interval.toString(); // 设置间隔  
            this.selectedHours.fill(false);
            this.buttonStates.fill('primary');
            this.maxAppointments = data.max_resnum.toString(); // 设置最大预约数  
            // 更新 selectedHours 根据 hour_0 到 hour_23 的值  
            for (let i = 0; i < 24; i++) {
                if (data[`hour_${i}`] === true){
                    this.selectedHours[i] = true;
                    this.buttonStates[i] = 'primary';
                    for (let k = 1; k < data.interval; k++) {
                        this.buttonStates[i + k] = 'warning';
                    }
                }
            };
        },  
    },
    mounted() {
        this.fetchAppointmentData(1,0);
    },
};  
</script>