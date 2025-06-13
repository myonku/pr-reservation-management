<template>
    <div class="col-lg-auto d-flex flex-column flex-shrink-0 p-3 text-bg-dark aside">
        <ul class="nav nav-pills flex-column mb-auto asideul">
            <li v-if="isHome" class="asidelink">
                <router-link :to="{ name: 'index' }" class="nav-link text-white" aria-current="page"
                    active-class="active">
                    概览
                </router-link>
            </li>
            <li v-if="isHome" class="asidelink">
                <a href="#" class="nav-link text-white" active-class="active">
                    最近记录
                </a>
            </li>
            <li v-if="isHome" class="asidelink">
                <a href="#" class="nav-link text-white">
                    我的预约
                </a>
            </li>


            <li v-if="isView" class="asidelink">
                <router-link :to="{ name: 'res_list' }" class="nav-link text-white" aria-current="page"
                    active-class="active">
                    待审核
                </router-link>
            </li>
            <li v-if="isView" class="asidelink">
                <router-link :to="{ name: 'all_list' }" class="nav-link text-white" active-class="active">
                    全部申请
                </router-link>
            </li>
            <li v-if="isView" class="asidelink">
                <router-link :to="{ name: 'serach' }" class="nav-link text-white" active-class="active">
                    查找
                </router-link>
            </li>
            <li v-if="isView" class="asidelink">
                <router-link :to="{ name: 'apd_list' }" class="nav-link text-white" active-class="active">
                    通过记录
                </router-link>
            </li>


            <li v-if="isManage" class="asidelink">
                <router-link :to="{ name: 'm_time' }" class="nav-link text-white" active-class="active">
                    时段管理
                </router-link>
            </li>
            <li v-if="isManage" class="asidelink">
                <router-link :to="{ name: 'm_device' }" class="nav-link text-white" active-class="active">
                    设备管理
                </router-link>
            </li>
            <li v-if="isManage" class="asidelink">
                <a href="#" class="nav-link text-white">
                    其他
                </a>
            </li>

            <li v-if="isCmt" class="asidelink">
                <router-link :to="{ name: 'user_cmt' }" class="nav-link text-white" active-class="active">
                    用户反馈
                </router-link>
            </li>
            <li v-if="isCmt" class="asidelink">
                <router-link :to="{ name: 'stf_cmt' }" class="nav-link text-white" active-class="active">
                    意见提交
                </router-link>
            </li>

            <li class="weali">
                <div class="weather">
                    <div class="d-flex">
                        <img id="icon" :src="iconUrl" alt="weather" width="46" height="46">
                        <div class="justify-content-center align-items-center">
                            <div class="d-flex">
                                <strong>
                                    <p style="margin-top:11px; font-size:120%">当前：</p>
                                </strong>
                                <strong>
                                    <p style="margin-top:11px; font-size:120%" id="description">{{
                                        weatherDescription }}
                                    </p>
                                </strong>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex">
                        <strong>
                        <p style="color:yellow;font-size:120%; padding-left:5px; border-bott" id="city">{{cityName}}</p>
                        </strong>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">当前气温：</p>
                        <p class="wec" id="temp">{{ temp }}</p>
                        <p class="wec">℃</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">体感温度：</p>
                        <p class="wec" id="feel_temp">{{ feelsTemp }}</p>
                        <p class="wec">℃</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">云量：</p>
                        <p class="wec" id="clouds">{{ clouds }}</p>
                        <p class="wec">%</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">气压：</p>
                        <p class="wec" id="pressure">{{ pressure }}</p>
                        <p class="wec">hPa</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">湿度：</p>
                        <p class="wec" id="humi">{{ humidity }}</p>
                        <p class="wec">%</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">风速：</p>
                        <p class="wec" id="wind">{{ windSpeed }}</p>
                        <p class="wec">米/秒</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">日出时间：</p>
                        <p class="wec" id="sunrise">{{ sunrise }}</p>
                    </div>
                    <div class="d-flex wec">
                        <p class="wec">日落时间：</p>
                        <p class="wec" id="sunset">{{ sunset }}</p>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: "aside",
    computed: {
        isManage() {
            return this.$route.path.startsWith('/main/manage');
        },
        isView() {
            return this.$route.path.startsWith('/main/view');
        },
        isHome() {
            return this.$route.path.startsWith('/main/home');
        },
        isCmt() {
            return this.$route.path.startsWith('/main/cmt');
        },
    },
    data() {
        return {
            city: "Suzhou",
            cityName: "苏州市",
            loading: true,
            temp: null,
            feelsTemp: null,
            pressure: null,
            humidity: null,
            windSpeed: null,
            weatherDescription: '',
            clouds: null,
            sunrise: '',
            sunset: '',
            iconUrl: '',
            intervalId: null,
        };
    },
    methods: {
        async getWeather() {
            this.loading = true; // 开始加载  
            try {
                let params = new URLSearchParams();
                params.append("city", this.city);
                const response = await axios.post(`http://127.0.0.1:8000/api/weather`, params);

                if (response.status !== 200) {
                    throw new Error('网络响应错误');
                }

                const data = response.data;
                this.temp = data.temp;
                this.feelsTemp = data.feels_temp;
                this.pressure = data.pressure;
                this.humidity = data.humi;
                this.windSpeed = data.wind.speed;
                this.weatherDescription = data.description;
                this.clouds = data.clouds;
                this.sunrise = data.sunrise;
                this.sunset = data.sunset;
                this.iconUrl = `https://openweathermap.org/img/w/${data.icon}.png`;
            } catch (error) {
                console.error('获取天气数据失败:', error);
            } finally {
                this.loading = false; // 结束加载  
            }
        },
    },
    mounted() {
        this.getWeather().then(() => {
            // 任务完成后发出事件  
            this.$emit('task-completed');
        })
            .catch(error => {
                console.error('获取天气数据时发生错误:', error);
            });; // 组件挂载后调用获取天气函数  

        this.intervalId = setInterval(this.getWeather, 180000);
    },
    beforeDestroy() {
        // 在组件销毁前清除定时器  
        clearInterval(this.intervalId);
    },
};  
</script>