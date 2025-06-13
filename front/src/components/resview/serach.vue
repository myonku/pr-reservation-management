<template>
    <div class="cardview">
        <div class="cardview_body">
            <h5 style="padding: 14px;">在这里查找具体的项，包括所有的预约申请和认证记录</h5>
            <div style="background-color: lightgray; padding: 8px; border-top: gray solid 1px;">
                <span class="badge rounded-pill bg-warning text-dark">注意</span>
                通过的预约申请不会归类于另外的通过记录并展示，而是同样显示初始预约申请，相关联的数据会显示在详情中。
            </div>
            <div style="padding: 8px;">
                根据输入的文本，搜索与之相关的记录，关联字段包括用户名、预约通道、用户备注等。<strong>每秒钟最多获取一次搜索数据。</strong>
            </div>
        </div>
        <div class="cardview_body">
            <div style="margin: 16px; padding: 20px;">
                <div class="row g-3 align-items-center">
                    <div class="col-auto">
                        <label for="inputText" class="col-form-label"><strong>输入关键字符获取记录：</strong>
                        </label>
                    </div>
                    <div class="col-lg-6">
                        <input type="text" id="inputText" class="form-control form-control" v-model="input"
                            aria-describedby="TextHelpInline" placeholder="输入文本..." maxlength="22"
                            :disabled="isDisabled" @blur="serachc()">
                    </div>
                    <div class="col-auto">
                        <span id="TextHelpInline" class="form-text text-end">
                            不应长于22个字符,已输入{{ char }}个字符
                        </span>
                    </div>
                    <div class="col-auto" v-if="isDisabled">
                        <el-progress :width="24" :stroke-width="4" type="circle" :percentage="percentage"
                            status="exception" />
                        <small style="padding-left: 10px; font-weight: bolder;">锁定中 - {{ second }}</small>
                    </div>

                </div>
                <hr style="border: 2px solid #0d6efd;">
                <div class="align-items-center align-middle" style="background-color: #f3f3f3;">
                    <div style="padding-top: 8px;">
                        <strong>日期与时间的限制的互相独立的，可以各自对应不同的字段，请留意切换按钮的状态</strong>
                        <div style="padding-top: 10px;">
                            <span class="badge rounded-pill bg-warning text-dark">!</span>
                            选中为“创建时间”时，对象将转向初始预约申请的创建时间，选中为“目标时间”时，对象则转向预约指向的开始时间。
                        </div>
                    </div>
                    <hr>
                    <div class="row" style="padding: 10px;padding-top: 0;">
                        <div class="col-lg-2" style="margin-top: 10px;">
                            选择日期范围
                        </div>
                        <div class="col-auto text-start">
                            <el-date-picker v-model="dateRange" type="daterange" start-placeholder="开始日期"
                                end-placeholder="结束日期" style="margin-top: 5px;" :disabled="isDisabled" />
                        </div>
                        <div class="col-auto text-start" style="margin-top: 10px;">
                            <small>此项只限制单独的任意仅<strong>日期</strong>部分</small>
                        </div>
                        <div class="col-lg-3 text-end" style="margin-top: 6px;">
                            锁定为:
                            <div class="btn-group" role="group" style="margin-left: 10px;"
                                aria-label="Basic radio toggle button group">
                                <input type="radio" class="btn-check" name="datesc" id="datesc1" v-model="datesc"
                                    value="1" autocomplete="off" checked :disabled="isDisabled" />
                                <label class="btn btn-outline-primary" for="datesc1">创建时间</label>

                                <input type="radio" class="btn-check" name="datesc" id="datesc2" v-model="datesc"
                                    value="2" autocomplete="off" :disabled="isDisabled" />
                                <label class="btn btn-outline-primary" for="datesc2">目标时间</label>
                            </div>
                        </div>
                    </div>


                    <div class="row" style="padding: 10px;">
                        <div class="col-lg-2" style="margin-top: 5px;">
                            选择时间范围
                        </div>
                        <div class="col-auto text-start">
                            <el-time-picker v-model="timeRange" is-range start-placeholder="开始时间" end-placeholder="结束时间"
                                style="margin-bottom: 5px;" :disabled="isDisabled" @blur="timerange_change" />
                        </div>
                        <div class="col-auto text-start" style="margin-top: 5px;">
                            <small>此项只限制单独的一天中<strong>时间</strong>部分</small>
                        </div>
                        <div class="col-lg-3 text-end">
                            锁定为:
                            <div class="btn-group" role="group" style="margin-left: 10px;"
                                aria-label="Basic radio toggle button group">
                                <input type="radio" class="btn-check" name="timesc" id="timesc1" v-model="timesc"
                                    value="1" autocomplete="off" checked :disabled="isDisabled" />
                                <label class="btn btn-outline-primary" for="timesc1">创建时间</label>

                                <input type="radio" class="btn-check" name="timesc" id="timesc2" v-model="timesc"
                                    value="2" autocomplete="off" :disabled="isDisabled" />
                                <label class="btn btn-outline-primary" for="timesc2">目标时间</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="margin: 10px;" class="align-items-center align-middle row">
                    <div class="col-lg-2"><strong>添加限制的通道</strong></div>
                    <div class="col-auto text-end">
                        <el-select-v2 v-model="value" :options="options" placeholder="选择通道" style="width: 340px"
                            multiple collapse-tags collapse-tags-tooltip :max-collapse-tags="3" clearable
                            :disabled="isDisabled" />
                    </div>
                    <div class="col-auto">
                        <el-tooltip content="获取最新的设备列表。如无必要，则不应频繁刷新" placement="bottom">
                            <button class="btn btn-info" @click="click_device_update()">刷新</button>
                        </el-tooltip>
                    </div>
                    <div class="col-lg-5 text-end">
                        分类:
                        <div class="btn-group" role="group" style="margin-left: 10px;"
                            aria-label="Basic radio toggle button group">
                            <input type="radio" class="btn-check" name="cate" id="cate0" value=0 v-model="cate"
                                autocomplete="off" checked :disabled="isDisabled" />
                            <label class="btn btn-outline-success" for="cate0">全部申请</label>

                            <input type="radio" class="btn-check" name="cate" id="cate1" value=1 v-model="cate"
                                autocomplete="off" :disabled="isDisabled" />
                            <label class="btn btn-outline-success" for="cate1">通道记录</label>
                        </div>
                    </div>
                </div>
            </div>
        </div><br>
        <div class="cardview_body">
            <h4 style="padding: 14px;" v-if="total">搜索结果</h4>
            <div v-if="isDisabled">
                <el-progress :width="24" :stroke-width="4" type="circle" :percentage="percentage" status="exception" />
                <small style="padding-left: 10px; font-weight: bolder;">锁定中 - {{ second }}</small>
            </div>
            <div style="margin: 15px;">
                <div class="row" v-if="total">
                    <div class="col-lg-4 text-start">&nbsp;共有<strong><span style="color: orange;">
                                {{ total }}</span></strong>条结果</div>
                    <div class="col-lg-8 text-end align-middle" style="padding-right: 30px;">
                        排序依据：
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1"
                                value="1" v-model="sortBy" checked :disabled="isDisabled">
                            <label class="form-check-label" for="inlineRadio1" checked>预约日期</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                                value="2" v-model="sortBy" :disabled="isDisabled">
                            <label class="form-check-label" for="inlineRadio2">创建时间</label>
                        </div>

                        &nbsp;&nbsp;
                        <div class="form-check form-switch form-check-inline">
                            <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault"
                                v-model="isDescending" checked :disabled="isDisabled">
                            <label class="form-check-label" for="flexSwitchCheckDefault"><strong>使用倒序排序</strong>
                            </label>
                        </div>
                    </div>
                </div>
                <table v-if="total" class="table table-hover table-striped"
                    style="padding-top: 12px;border-top:1px lightgray solid">
                    <thead>
                        <tr>
                            <th class="sorting" scope="col">序号</th>
                            <th class="sorting" scope="col">用户</th>
                            <th class="sorting" scope="col">预约日期</th>
                            <th class="sorting" scope="col">预约时间段</th>
                            <th class="sorting" scope="col">预约通道</th>
                            <th class="sorting" scope="col">邀请人</th>
                            <th class="sorting" scope="col">标签</th>
                            <th class="sorting" scope="col">操作</th>
                        </tr>
                    </thead>

                    <tbody id="vlist">
                        <tr v-for="(item, index) in items" :key="item.id">
                            <th class="tbr align-middle" scope="row">{{ index + 1 + current_start }}</th>
                            <td class="tbr align-middle">
                                <img title="用户" :src="`http://127.0.0.1:8000${item.res_user.profile}`" alt="avatar"
                                    width="26" height="26" class="rounded-circle me-2" />
                                {{ item.res_user?.username || '无' }}
                            </td>
                            <td class="tbr align-middle">{{ item.res_start_time.substr(0, 10) }}</td>
                            <td class="tbr align-middle">{{ item.res_start_time.slice(-5) }} - {{
                                item.res_dec_time.slice(-5) }}</td>
                            <td class="tbr align-middle">{{ item.device.name }}</td>
                            <td class="tbr align-middle">{{ item.inviter?.username || '无' }}</td>
                            <td class="tbr align-middle">
                                <template v-if="item.state === '待审核'">
                                    <span class="badge bg-warning">待审</span>
                                </template>
                                <template v-else-if="item.state === '已通过'">
                                    <span class="badge bg-success">通过</span>
                                </template>
                                <template v-else-if="item.state === '未通过'">
                                    <span class="badge bg-danger">拒绝</span>
                                </template>
                                <template v-else-if="item.state === '已过期'">
                                    <span class="badge bg-secondary">过期</span>
                                </template>

                                <template v-if="item.apd_ori_resvation[0]!= null">
                                    &nbsp;
                                    <template v-if="item.apd_ori_resvation[0].state_apd === '未生效'">
                                        <span class="badge bg-info">未生效</span>
                                    </template>
                                    <template v-else-if="item.apd_ori_resvation[0].state_apd === '待认证'">
                                        <span class="badge bg-primary">待认证</span>
                                    </template>
                                    <template v-else-if="item.apd_ori_resvation[0].state_apd === '已认证'">
                                        <span class="badge bg-success">已认证</span>
                                    </template>
                                    <template v-else-if="item.apd_ori_resvation[0].state_apd === '已过期'">
                                        <span class="badge bg-secondary">已过期</span>
                                    </template>
                                </template>

                            </td>
                            <td>
                                <button class="btn btn-primary btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#staticBackdrop" @click="set_dialog_item(item.id)">查看</button>&nbsp;
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false"
                    tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="staticBackdropLabel">查看记录</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <h5>您无权限修改此项内容</h5>
                                <el-descriptions title="记录内容">
                                    <el-descriptions-item label="记录ID">{{ v_id }}</el-descriptions-item>
                                    <el-descriptions-item label="提交者">{{ v_user }}</el-descriptions-item>
                                    <el-descriptions-item label="提交时间">{{ v_res_time }}</el-descriptions-item>
                                    <el-descriptions-item label="审核于">{{ v_pr_time }}</el-descriptions-item>
                                    <el-descriptions-item label="审核人">{{ v_pr_user }}</el-descriptions-item>
                                    <el-descriptions-item label="状态">
                                        <el-tag size="small" :type="type">{{ v_tag }}</el-tag>
                                        <span v-if="v_tag_d">&nbsp;&nbsp;</span>
                                        <el-tag v-if="v_tag_d" size="small" :type="type1">{{ v_tag_d }}</el-tag>
                                    </el-descriptions-item>

                                    <el-descriptions-item label="通道">{{ v_device }}</el-descriptions-item>
                                    <el-descriptions-item label="目标日期">{{ v_date }}</el-descriptions-item>
                                    <el-descriptions-item label="目标时间段">{{ v_time }}</el-descriptions-item>
                                    <el-descriptions-item label="通过时间">{{ v_cmp_time }}</el-descriptions-item>
                                    <el-descriptions-item label="备注">{{ v_desc }}</el-descriptions-item>
                                </el-descriptions>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">关闭</button>
                            </div>
                        </div>
                    </div>
                </div>
                <br>
                <nav class="pages" aria-label="Page navigation example">

                    <ul v-if="is_paginated" class="pagination justify-content-center" id="nav">
                        <li v-if="if_has_previous" class="page-item"
                            :class="{ disabled: !if_has_previous || isDisabled }">
                            <a class="page-link" href="javascript:void(0)"
                                @click="if_has_previous && get_search_result(pagenum - 1)">上一页</a>
                        </li>
                        <li v-else class="page-item disabled"><span class="page-link">上一页</span></li>
                        
                        <li class="page-item" v-for="(i, index) in pages" :key="index"
                            :class="{ active: i === pagenum, disabled: i == disable_page || isDisabled }">
                            <a class="page-link" href="javascript:void(0)" @click="get_search_result(i)">{{ i }}</a>
                        </li>

                        <li v-if="if_has_next" class="page-item" :class="{ disabled: !if_has_next || isDisabled }">
                            <a class="page-link" href="javascript:void(0)"
                                @click="if_has_next && get_search_result(pagenum + 1)">下一页</a>
                        </li>
                        <li v-else class="page-item disabled"><span class="page-link">下一页</span></li>
                    </ul>
                </nav>
            </div>

        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { ElMessage } from 'element-plus'
export default {
    data() {
        return {
            cate: 0,
            datesc: '1',
            timesc: "1",
            input: '',
            oldinput: '',
            oldrange: '',
            char: 0,
            dateRange: [],
            timeRange: [],
            options: [],
            value: [],
            //
            pagenum: 1, // 当前页码 
            total: 0, //内容总个数
            sortBy: '1', // 默认排序依据为预约日期  
            isDescending: true, // 默认使用倒序  
            num_page: 0, // 总页数  
            is_paginated: false,
            items: [], // 用于存储结果数据   
            current_start: 0, // 当前起始记录  
            if_has_previous: false, // 是否有上一页  
            if_has_next: false, // 是否有下一页  
            page_last: 0,  //最后一页的页码，也就是总页数
            isDisabled: false,
            second: 1, // 倒计时初始值  
            percentage: 0, // 进度条初始值  
            timer: null, // 存储定时器的引用  
            ////
            v_user: "",
            v_res_time: '',
            v_pr_time: '',
            v_tag: '',
            v_device: '',
            v_date: '',
            v_time: '',
            v_cmp_time: '',
            v_pr_user: '',
            v_desc: '',
            v_id: '',
            type: null,
            type1: null,
            pages: [1],
            disable_page: "...",
        }
    },
    methods: {
        update_page(){
            const page_num = this.pagenum;
            const page_total = this.page_last;
            const pg = [];
            if (page_total <= 7){
                for(let i=1; i<=page_total; i++){
                    pg.push(i)
                }
            }else{
                const middle = page_total / 2;
                const pre_all = page_num;   //前方总页
                const fd_all = page_total - page_num + 1;  //后方总页
                if (page_num <= middle){
                    
                    if(pre_all <= 4){
                        for (let i = 1; i <= 4; i++) {
                            pg.push(i);
                        }
                        pg.push(5);
                        pg.push("...");
                        pg.push(page_total);
                    }else{
                        pg.push(1);
                        pg.push("...");
                        pg.push(page_num -1);
                        pg.push(page_num);
                        pg.push(page_num + 1);
                        pg.push("...");
                        pg.push(page_total);
                    }

                }else{
                    
                    if(fd_all <= 4){
                        pg.push(1);
                        pg.push("...");
                        const rest = 7 - fd_all;
                        if(rest == 4){
                            pg.push(page_num - 2);
                        }else if(rest == 5){
                            pg.push(page_num - 3);
                            pg.push(page_num - 2);
                        } else if (rest == 6) {
                            pg.push(page_num - 4);
                            pg.push(page_num - 3);
                            pg.push(page_num - 2);
                        }
                        pg.push(page_num - 1);
                        for (let i = page_num; i <= page_total; i++) {
                            pg.push(i);
                        }
                    }else{
                        pg.push(1);
                        pg.push("...");
                        pg.push(page_num - 1);
                        pg.push(page_num);
                        pg.push(page_num + 1);
                        pg.push("...");
                        pg.push(page_total);
                    }
                }
            };
            this.pages = pg;
        },
        async set_dialog_item(i) {
            try {
                let params = new URLSearchParams();
                params.append("id", i);
                params.append("key", 0);
                const response = await axios.post("http://127.0.0.1:8000/api/get_record_detail", params);

                const origin_resvation = response.data; // 假设后端返回的是 JSON 格式  
                this.v_id = origin_resvation.id;
                this.v_user = origin_resvation.res_user.username;
                this.v_res_time = origin_resvation.res_time;
                this.v_pr_time = origin_resvation.audit_time || "未审核";
                this.v_pr_user = origin_resvation.audit_staff?.username || '无'
                
                this.v_tag = origin_resvation.state;
                //this.v_tag_d = origin_resvation.s;
                if (this.v_tag == "待审核") {
                    this.type = "warning";
                } else if (this.v_tag == "已通过") {
                    this.type = "success";
                } else if (this.v_tag == "未通过") {
                    this.type = "danger";
                } else {
                    this.type = "info";
                }
                if (origin_resvation.apd_ori_resvation.length != 0) {
                    this.v_tag_d = origin_resvation.apd_ori_resvation[0].state_apd;
                    if (this.v_tag_d == "待生效") {
                        this.type1 = "primary";
                    } else if (this.v_tag_d == "待认证") {
                        this.type1 = "warning";
                    } else if (this.v_tag_d == "已认证") {
                        this.type1 = "success";
                    } else {
                        this.type = "info";
                    }
                } else {
                    this.v_tag_d = null;
                }
                this.v_device = origin_resvation.device.name;
                this.v_date = origin_resvation.res_start_time.substr(0, 10);
                this.v_time = origin_resvation.res_start_time.slice(-5) + "--" + origin_resvation.res_dec_time.slice(-5);
                if (origin_resvation.apd_ori_resvation.length > 0){
                    this.v_cmp_time = origin_resvation.apd_ori_resvation[0].completed_time || "未通过";
                }else{
                    this.v_cmp_time = "未通过"
                }
                
                this.v_desc = origin_resvation.description;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始  
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        formatTime(date) {
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            return `${hours}:${minutes}`;
        },
        async click_device_update(){
            try{
                this.get_all_dev();
                ElMessage({
                    message: '数据刷新成功',
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
        },
        async timerange_change() {
            if (!this.input.trim() || this.oldrange === this.timeRange) {
                return;
            }
            this.oldrange = this.timeRange;
            this.get_search_result();
        },
        async get_all_dev() {
            try {
                const response = await axios.post(`http://127.0.0.1:8000/api/get_all_dev`, { "key": 1 });
                if (response.data.list && Array.isArray(response.data.list)) {
                    this.options = response.data.list.map(name => ({
                        label: name,
                        value: name, // 这里要确保 label 和 value 的一致性  
                    }));
                } else {
                    console.error("无效的数据格式：", response.data);
                }

            } catch (error) {
                console.error('获取数据失败:', error);
            }
        },
        async serachc(){
            if (!this.input.trim() || this.oldinput === this.input) {
                return;
            }
            this.oldinput = this.input;
            this.get_search_result();
        },
        async get_search_result(page_num = 1) {

            if (!this.input.trim()) {
                return;
            }
            this.isDisabled = true;

            const totalDuration = 1000; // 总时间 1 秒  
            const intervalDuration = 100; // 每 100 毫秒更新  
            const totalSteps = totalDuration / intervalDuration; // 总步数  
            let step = 0; // 当前步数  

            // 启动定时器  
            this.timer = setInterval(() => {
                let i = 1
                step++;
                i = 1 - (step * intervalDuration) / 1000; // 更新倒计时 
                this.second = i.toFixed(1)
                this.percentage = (step / totalSteps) * 100; // 更新进度条  

                // 达到总步数时清除定时器  
                if (step >= totalSteps) {
                    clearInterval(this.timer); // 清除定时器  
                }
            }, intervalDuration); // 每 100 毫秒更新  

            setTimeout(() => {
                this.isDisabled = false; // 恢复状态  
                clearInterval(this.timer); // 确保清除定时器  
                this.second = 0; // 重置倒计时  
                this.percentage = 0; // 重置进度条  
            }, 1000); // 1秒后恢复 

            let dateRangex = this.dateRange;
            let timeRangex = this.timeRange;
            if (this.dateRange.length === 2) {
                const startDate = new Date(this.dateRange[0]);
                const endDate = new Date(this.dateRange[1]);
                dateRangex = [this.formatDate(startDate), this.formatDate(endDate)];
            }
            if (this.timeRange.length === 2) {
                const startTime = new Date(this.timeRange[0]);
                const endTime = new Date(this.timeRange[1]);
                timeRangex = [this.formatTime(startTime), this.formatTime(endTime)];
            }
            let params = new URLSearchParams();
            params.append("page_num", page_num);
            params.append("input", this.input);
            params.append("datesc", this.datesc);
            params.append("timesc", this.timesc);
            params.append("dateRange", dateRangex);
            params.append("timeRange", timeRangex);
            params.append("value", this.value);
            params.append("cate", this.cate);
            params.append("sortBy", this.sortBy);
            params.append("isDescending", this.isDescending);
            try {
                const response = await axios.post(`http://127.0.0.1:8000/api/get_search_result`, params);
                const data = response.data; // 假设后端返回的是 JSON 格式  
                this.items = data.page; // 更新结果数据  
                this.pagenum = data.pagenum; // 更新当前页码  
                this.page_last = data.page_last; // 设置总页数  
                this.current_start = data.current_start; // 设置当前起始记录  
                this.if_has_previous = data.if_has_previous; // 设置是否有上一页  
                this.if_has_next = data.if_has_next; // 设置是否有下一页  
                this.is_paginated = data.is_paginated;
                this.total = data.total;
                this.update_page();
            } catch (error) {
                console.error('获取数据失败:', error);
            }
        }
    },
    mounted() {
        this.get_all_dev();
        this.input = this.$route.query.keyword || ''; // 默认值为空字符串  
        if (this.input) {
            this.get_search_result(); // 如果有关键字，则调用搜索  
        }
    },
    watch: {
        input(newVal) {
            this.char = newVal.length;
        },
        sortBy(newVal, oldVal) {
            if (this.total > 1) {
                this.get_search_result(this.pagenum); // 当 sortBy 改变时调用方法  
            } else {
                return;
            }
        },
        isDescending(newVal, oldVal) {
            if (this.total > 1) {
                this.get_search_result(this.pagenum); // 当 isDescending 改变时调用方法  
            } else {
                return;
            }
        },
        cate(newVal, oldVal) {
            if (this.input.trim()) {
                this.get_search_result(this.pagenum)
            } else {
                return
            }
        },
        datesc(newVal, oldVal) {
            if (this.input.trim()) {
                this.get_search_result(this.pagenum)
            } else {
                return
            }
        },
        timesc(newVal, oldVal) {
            if (this.input.trim()) {
                this.get_search_result(this.pagenum)
            } else {
                return
            }
        },
        dateRange(newVal, oldVal) {
            if (this.input.trim()) {
                this.get_search_result(this.pagenum)
            } else {
                return
            }
        },
        value(newVal, oldVal) {
            if (this.input.trim()) {
                this.get_search_result(this.pagenum)
            } else {
                return
            }
        },
    },
}
</script>