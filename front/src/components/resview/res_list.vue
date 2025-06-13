<template>
    <div class="cardview">
        <div class="cardview_body" v-loading="fullscreenLoading">
            <div style="padding-top:30px; padding-bottom:16px; width: 100%;">
                <h5>所有的待审核的预约申请记录。只显示状态为“待审核”的记录，已过期或已经经过审核的记录将不会在此显示</h5>
                <hr>
                <div>
                    如果需要更精确地局限范围，请前往 <router-link :to="{ name: 'serach' }">查找</router-link> 页面
                </div>
            </div>
        </div>

        <div class="cardview_body">
            <div style="margin:20px">
                <br>
                <div class="row" v-if="total">
                    <div class="col-lg-4 text-start">&nbsp;共有<strong><span style="color: orange;">{{ total
                                }}</span></strong>条记录</div>
                    <div class="col-lg-8 text-end align-middle" style="padding-right: 30px;">
                        排序依据：
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1"
                                value="1" v-model="sortBy" checked>
                            <label class="form-check-label" for="inlineRadio1" checked>预约日期</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                                value="2" v-model="sortBy">
                            <label class="form-check-label" for="inlineRadio2">创建时间</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3"
                                value="3" v-model="sortBy">
                            <label class="form-check-label" for="inlineRadio3">失效时间</label>
                        </div>
                        &nbsp;&nbsp;
                        <div class="form-check form-switch form-check-inline">
                            <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault"
                                v-model="isDescending" checked>
                            <label class="form-check-label" for="flexSwitchCheckDefault"><strong>使用倒序排序</strong>
                            </label>
                        </div>
                    </div>
                </div><br>
                <table class="table table-hover table-striped" style="padding-top: 12px;border-top:1px lightgray solid">
                    <thead>
                        <tr>
                            <th class="sorting" scope="col">序号</th>
                            <th class="sorting" scope="col">用户</th>
                            <th class="sorting" scope="col">记录ID</th>
                            <th class="sorting" scope="col">预约日期</th>
                            <th class="sorting" scope="col">预约时间段</th>
                            <th class="sorting" scope="col">预约通道</th>
                            <th class="sorting" scope="col">申请失效时间</th>
                            <th class="sorting" scope="col">邀请人</th>
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
                            <td class="tbr align-middle">{{ item.id }}</td>
                            <td class="tbr align-middle">{{ item.res_start_time.substr(0, 10) }}</td>
                            <td class="tbr align-middle">{{ item.res_start_time.slice(-5) }} - {{
                                item.res_dec_time.slice(-5) }}</td>
                            <td class="tbr align-middle">{{ item.device.name }}</td>
                            <td class="tbr align-middle">{{ item.res_end_time }}</td>
                            <td class="tbr align-middle">{{ item.inviter?.username || '无' }}</td>
                            <td>
                                <button class="btn btn-primary btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#staticBackdrop" @click="set_dialog_item(item.id)">查看</button>&nbsp;
                                <button class="btn btn-warning btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#staticBackdrop1" @click="set_id(item.id)">拒绝</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
                aria-labelledby="staticBackdropLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="staticBackdropLabel">待审记录</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h5>您无权限修改此项内容</h5>
                            <el-descriptions title="记录内容">
                                <el-descriptions-item label="记录ID">{{ v_id }}</el-descriptions-item>
                                <el-descriptions-item label="提交者">{{ v_user }}</el-descriptions-item>
                                <el-descriptions-item label="提交时间">{{ v_res_time }}</el-descriptions-item>

                                <el-descriptions-item label="通道">{{ v_device }}</el-descriptions-item>
                                <el-descriptions-item label="目标日期">{{ v_date }}</el-descriptions-item>
                                <el-descriptions-item label="目标时间段">{{ v_time }}</el-descriptions-item>
                                <el-descriptions-item label="备注">{{ v_desc }}</el-descriptions-item>
                            </el-descriptions>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-warning" data-bs-dismiss="modal"
                                @click="asc_record(this.v_id, 0)">批准申请</button>
                            <span style="width: 20px;"></span>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false"
                tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="staticBackdropLabel">待审记录</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <h5>确定拒绝该条预约申请吗？一旦拒绝，将无法撤销。</h5>
                            <hr>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                                @click="asc_record(this.v_id, 1)">拒绝申请</button>
                            <span style="width: 20px;"></span>
                            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>

            <nav class="pages" aria-label="Page navigation example">

                <ul v-if="is_paginated" class="pagination justify-content-center" id="nav">
                    <li v-if="if_has_previous" class="page-item" :class="{ disabled: !if_has_previous }">
                        <a class="page-link" href="javascript:void(0)"
                            @click="if_has_previous && get_res_list(pagenum - 1)">上一页</a>
                    </li>
                    <li v-else class="page-item disabled"><span class="page-link">上一页</span></li>
                    <li class="page-item" v-for="(i, index) in pages" :key="index"
                        :class="{ active: i === pagenum, disabled: i == disable_page }">
                        <a class="page-link" href="javascript:void(0)" @click="get_res_list(i)">{{ i }}</a>
                    </li>
                    <li v-if="if_has_next" class="page-item" :class="{ disabled: !if_has_next }">
                        <a class="page-link" href="javascript:void(0)"
                            @click="if_has_next && get_res_list(pagenum + 1)">下一页</a>
                    </li>
                    <li v-else class="page-item disabled"><span class="page-link">下一页</span></li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { ElNotification } from 'element-plus'
export default {
    data() {
        return {
            fullscreenLoading: false,
            total: 0,
            sortBy: '1', // 默认排序依据为预约日期  
            isDescending: true, // 默认使用倒序  
            pagekey: 1,
            num_page: 0, // 总页数  
            pagenum: 1, // 当前页码  
            is_paginated: false,
            items: [], // 用于存储结果数据   
            current_start: 0, // 当前起始记录  
            if_has_previous: false, // 是否有上一页  
            if_has_next: false, // 是否有下一页  
            page_last: 0,
            refreshInterval: null, // 用于存储定时器 ID
            //
            v_user: "",
            v_res_time: '',
            v_device: '',
            v_date: '',
            v_time: '',
            v_desc: '',
            v_id: '',
            pages: [1],
            disable_page: "...",
        };
    },
    watch: {
        sortBy(newVal, oldVal) {
            if (this.total > 1) {
                this.get_res_list(this.pagenum); // 当 sortBy 改变时调用方法  }
            }else{
                return
            }
        },
        isDescending(newVal, oldVal) {
            if (this.total > 1) {
                this.get_res_list(this.pagenum); // 当 sortBy 改变时调用方法  }
            } else {
                return
            }
        }
    },
    methods: {
        set_id(i){
            this.v_id = i;
        },
        update_page() {
            const page_num = this.pagenum;
            const page_total = this.page_last;
            const pg = [];
            if (page_total <= 7) {
                for (let i = 1; i <= page_total; i++) {
                    pg.push(i)
                }
            } else {
                const middle = page_total / 2;
                const pre_all = page_num;   //前方总页
                const fd_all = page_total - page_num + 1;  //后方总页
                if (page_num <= middle) {

                    if (pre_all <= 4) {
                        for (let i = 1; i <= 4; i++) {
                            pg.push(i);
                        }
                        pg.push(5);
                        pg.push("...");
                        pg.push(page_total);
                    } else {
                        pg.push(1);
                        pg.push("...");
                        pg.push(page_num - 1);
                        pg.push(page_num);
                        pg.push(page_num + 1);
                        pg.push("...");
                        pg.push(page_total);
                    }

                } else {

                    if (fd_all <= 4) {
                        pg.push(1);
                        pg.push("...");
                        const rest = 7 - fd_all;
                        if (rest == 4) {
                            pg.push(page_num - 2);
                        } else if (rest == 5) {
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
                    } else {
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
        async asc_record(i, k){
            this.fullscreenLoading = true;
            const token = sessionStorage.getItem('token'); // 从sessionStorage中获取token  
            let params = new URLSearchParams();
            params.append("id", i);
            params.append("manage", k);
            params.append("token", token);
            try{
                const response = await axios.post("http://127.0.0.1:8000/api/asc_record", params);
                const data = response.data;
                const key = data.key;
                const context = data.context;
                const type = key == 0 ? "success" : "error";
                this.fullscreenLoading = false;
                ElNotification({
                    title: '系统消息',
                    message: context,
                    type: type,
                    position: 'bottom-right',
                });
                this.get_res_list(this.pagenum);
            }catch{
                this.fullscreenLoading = false;
                ElNotification({
                    title: '系统消息',
                    message: "操作失败！请检查网络后重试。",
                    type: "error",
                    position: 'bottom-right',
                })
            }
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
 
                this.v_device = origin_resvation.device.name;
                this.v_date = origin_resvation.res_start_time.substr(0, 10);
                this.v_time = origin_resvation.res_start_time.slice(-5) + "--" + origin_resvation.res_dec_time.slice(-5);
                this.v_desc = origin_resvation.description;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async get_res_list(page_num = 1) {

            const pagekey = this.pagekey;
            let params = new URLSearchParams();
            params.append("key", pagekey);
            params.append("page_num", page_num);
            params.append("sortBy", this.sortBy);
            params.append("isDescending", this.isDescending);

            try {
                const response = await axios.post("http://127.0.0.1:8000/api/v_res_list", params);

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
                console.error('Error fetching data:', error);
            }
        },
        startRefresh() {
            this.refreshInterval = setInterval(() => {
                this.get_res_list(this.pagenum); // 每分钟刷新当前页的数据  
            }, 120000); // 60000 毫秒 = 1 分钟  
        },
        stopRefresh() {
            clearInterval(this.refreshInterval); // 清除定时器  
        }
    },
    mounted() {
        this.get_res_list(); // 组件挂载后获取初始数据  
        this.startRefresh(); // 启动数据刷新  
    },
    beforeDestroy() {
        this.stopRefresh(); // 组件销毁前清除定时器  
    }
};  
</script>