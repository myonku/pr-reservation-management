<template>
    <link href="./src/assets/css/album.css" rel="stylesheet">
    <link href="./src/assets/css/pricing.css" rel="stylesheet">

    <div style="width: 100%;">
        <div class="cardview_body">
            <div style="padding: 14px;border-bottom: 1px solid lightgray;">
                <h4>开始对接下来几天的通过申请的管理、安排合适的预约时间段和其他事务</h4>
            </div>
        </div><br>
        <div class="row cardview_body" style="padding-top: 20px;margin: 0;">
            <div class="col-lg-10 text-end">
                <div class="btn-group">
                    <input type="radio" class="btn-check" name="n" id="n1" v-model="selectTimefor" value="0"
                        autocomplete="off" checked />
                    <label class="btn btn-outline-primary btn-sm" for="n1">申请时间</label>

                    <input type="radio" class="btn-check" name="n" id="n2" v-model="selectTimefor" value="1"
                        autocomplete="off" />
                    <label class="btn btn-outline-primary btn-sm" for="n2">目标时间</label>
                </div>
            </div>
            <div class="col-lg-2 text-start">
                <div class="btn-group">
                    <input type="radio" class="btn-check" name="k" id="k1" v-model="selectTimein" value="7"
                        autocomplete="off" />
                    <label class="btn btn-outline-secondary btn-sm" for="k1">7天</label>

                    <input type="radio" class="btn-check" name="k" id="k2" v-model="selectTimein" value="30"
                        autocomplete="off" checked />
                    <label class="btn btn-outline-secondary btn-sm" for="k2">30天</label>

                    <input type="radio" class="btn-check" name="k" id="k3" v-model="selectTimein" value="90"
                        autocomplete="off" />
                    <label class="btn btn-outline-secondary btn-sm" for="k3">90天</label>
                </div>
            </div>
        </div>
        <div class="cardview_body" id="myChart-line" style="height: 400px;width: 100%; padding-left:15px">
        </div>
        <br>
        <div class="row cardview_body" style="padding-top: 20px;margin: 0;">
            <div class="col-lg-6 text-end">
                <div class="btn-group">
                    <input type="radio" class="btn-check" name="v" id="v1" v-model="selectTimein1" value="7"
                        autocomplete="off" />
                    <label class="btn btn-outline-primary btn-sm" for="v1">7天</label>

                    <input type="radio" class="btn-check" name="v" id="v2" v-model="selectTimein1" value="30"
                        autocomplete="off" checked />
                    <label class="btn btn-outline-primary btn-sm" for="v2">30天</label>

                    <input type="radio" class="btn-check" name="v" id="v3" v-model="selectTimein1" value="90"
                        autocomplete="off" />
                    <label class="btn btn-outline-primary btn-sm" for="v3">90天</label>
                </div>
            </div>
            <div class="col-lg-6 text-end">
                <div class="btn-group">
                    <input type="radio" class="btn-check" name="z" id="z1" v-model="selectTimein2" value="7"
                        autocomplete="off" />
                    <label class="btn btn-outline-primary btn-sm" for="z1">7天</label>

                    <input type="radio" class="btn-check" name="z" id="z2" v-model="selectTimein2" value="30"
                        autocomplete="off" checked />
                    <label class="btn btn-outline-primary btn-sm" for="z2">30天</label>

                    <input type="radio" class="btn-check" name="z" id="z3" v-model="selectTimein2" value="90"
                        autocomplete="off" />
                    <label class="btn btn-outline-primary btn-sm" for="z3">90天</label>
                </div>
            </div>
        </div>
        <div class="row center-block" style="margin:0px">

            <div class="cardview_body col-auto text-center" id="myChart-histogram"
                style="padding-top:30px;width:50%;height: 400px;border-right:2px solid #f3f3f3"></div>
            <div class="cardview_body col-auto text-right" id="myChart-pie"
                style="padding-top:30px;width: 50%;height:400px; padding-left: 65px;"></div>
        </div>

        <div style="height: 40px;"></div>
    </div>
</template>
<script>

import axios from 'axios';
import * as echarts from 'echarts'; // 确保您已安装 echarts  

export default {
    data() {
        return {
            refreshInterval: null, // 用于存储定时器 ID
            selectTimein: '30',
            selectTimefor: '0',
            selectTimein1: '30',
            selectTimein2: '30',
        };
    },
    methods: {
        getDays(x) {
            const dates = [];
            const today = new Date();
            for (let i = 0; i < x; i++) {
                const date = new Date(today);
                date.setDate(today.getDate() - i);
                const formattedDate = date.toISOString().split('T')[0];
                dates.push(formattedDate);
            }
            return dates.reverse();
        },
        async getChart1() {
            const sc = Number(this.selectTimein);
            let params = new URLSearchParams();
            params.append("day", this.selectTimein);
            params.append("for", this.selectTimefor);

            axios.post('http://127.0.0.1:8000/api/charts1', params).then(response => {
                const chartdata = response.data; // 假设后端直接返回 JSON 格式  
                // 绘制折线图  
                const myChartLine = echarts.init(document.getElementById('myChart-line'));
                myChartLine.setOption({
                    title: {
                        text: '最近预约数量分布'
                    },
                    xAxis: {
                        type: 'category',
                        data: this.getDays(sc)
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [{
                        data: chartdata,
                        type: 'line'
                    }]
                });
            }).catch(error => {
                console.error('Error fetching charts data:', error);
            });
        },
        async getChart2() {
            let params = new URLSearchParams();
            params.append("day", this.selectTimein1);
            // 绘制柱状图  
            axios.post('http://127.0.0.1:8000/api/charts2', params).then(response => {
                const chartdata = response.data; // 假设后端直接返回 JSON 格式  
                const myChartHistogram = echarts.init(document.getElementById('myChart-histogram'));
                myChartHistogram.setOption({
                    title: {
                        text: '各时段预约数量'
                    },
                    tooltip: {},
                    legend: {
                        data: ['预约量']
                    },
                    xAxis: {
                        data: ["0：00-3：00", "3：00-6：00", "6：00-9：00", "9：00-12：00", "12：00-15：00", "15:00-18:00", "18:00-21:00", "21:00-24：00"]
                    },
                    yAxis: {},
                    series: [{
                        name: '预约量',
                        type: 'bar',
                        data: chartdata,
                    }]
                });
            }).catch(error => {
                console.error('Error fetching charts data:', error);
            });
        },
        async getChart3() {
            let params = new URLSearchParams();
            params.append("day", this.selectTimein2);
            // 绘制饼图  
            axios.post('http://127.0.0.1:8000/api/charts3', params).then(response => {
                const chartdata = response.data;
                const myChartPie = echarts.init(document.getElementById('myChart-pie'));
                const pieData = chartdata.count.map((count, index) => ({
                    value: count,
                    name: chartdata.names[index]
                }));

                myChartPie.setOption({
                    title: {
                        text: '预约通道分布',
                        x: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        data: chartdata.names,
                    },
                    series: [{
                        name: '通道设备',
                        type: 'pie',
                        radius: '55%',
                        center: ['50%', '60%'],
                        data: pieData,
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                });
            }).catch(error => {
                console.error('Error fetching charts data:', error);
            });
        },
        startRefresh() {
            this.getChart1();
            this.getChart2();
            this.getChart3();
            this.refreshInterval = setInterval(() => {
                // 每分钟刷新当前页的数据  
                this.getChart1();
                this.getChart2();
                this.getChart3();
            }, 180000); // 60000 毫秒 = 1 分钟  
        },
        stopRefresh() {
            clearInterval(this.refreshInterval); // 清除定时器  
        }
    },
    watch: {
        selectTimein(newVal, oldVal) {
            this.getChart1();
        },
        selectTimefor(newVal, oldVal) {
            this.getChart1();
        },
        selectTimein1(newVal, oldVal) {
            this.getChart2();
        },
        selectTimein2(newVal, oldVal) {
            this.getChart3();
        },
    },
    mounted() {

        this.startRefresh(); // 启动数据刷新  
    },
    beforeDestroy() {
        this.stopRefresh(); // 组件销毁前清除定时器  
    }
};  
</script>