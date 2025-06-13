<template>
    <div class="cardview">
        <div class="cardview_body">
            <div style="padding-top:30px; padding-bottom:16px; width: 100%;">
                <div>
                    <h5>这里列出所有的预约申请记录，但不包括申请通过后的通过记录（此项在搜索页面中同样可以检索）</h5>
                    <hr>
                    <div>
                        如果需要更精确地局限范围，请前往 <router-link :to="{ name: 'serach' }">查找</router-link> 页面
                    </div>
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
                </div>

                <br>
                <table class="table table-hover table-striped"
                    style="padding-left: 10px;padding-right: 10px;padding-top: 12px; border-top:1px lightgray solid">
                    <thead>
                        <tr>
                            <th scope="col">序号</th>
                            <th scope="col">用户</th>
                            <th scope="col">记录ID</th>
                            <th scope="col">预约日期</th>
                            <th scope="col">预约时段</th>
                            <th scope="col">预约通道</th>
                            <th scope="col">状态</th>
                            <th scope="col">审核员</th>
                            <th scope="col">邀请人</th>
                            <th scope="col">操作</th>
                        </tr>
                    </thead>

                    <tbody id="vlist" class="all_tb">
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
                                <template v-else>
                                    <span class="badge bg-secondary">过期</span>
                                </template>
                            </td>
                            <td class="tbr align-middle">{{ item.audit_staff?.username || '无' }}</td>
                            <td class="tbr align-middle">{{ item.inviter?.username || '无' }}</td>
                            <td>
                                <button class="btn btn-info btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#staticBackdrop" @click="set_dialog_item(item.id)">查看</button>
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
                            <h5 class="modal-title" id="staticBackdropLabel">申请记录</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
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

export default {
    data() {
        return {
            total: 0,
            sortBy: '1', // 默认排序依据为预约日期  
            isDescending: true, // 默认使用倒序 
            pagekey: 0,
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
            pages: [1],
            disable_page: "...",
        };
    },
    watch: {
        sortBy(newVal, oldVal) {
            if (this.total > 1) {
                this.get_res_list(this.pagenum); // 当 sortBy 改变时调用方法  
            } else {
                return
            }
        },
        isDescending(newVal, oldVal) {
            if (this.total > 1) {
                this.get_res_list(this.pagenum); // 当 sortBy 改变时调用方法  
            } else {
                return
            } 
        }
    },
    methods: {
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
                if (this.v_tag == "待审核") {
                    this.type = "warning";
                } else if (this.v_tag == "已通过") {
                    this.type = "success";
                } else if (this.v_tag == "未通过") {
                    this.type = "danger";
                } else {
                    this.type = "info";
                }
                this.v_device = origin_resvation.device.name;
                this.v_date = origin_resvation.res_start_time.substr(0, 10);
                this.v_time = origin_resvation.res_start_time.slice(-5) + "--" + origin_resvation.res_dec_time.slice(-5);
                this.v_cmp_time = origin_resvation.completed_time || "未通过";
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