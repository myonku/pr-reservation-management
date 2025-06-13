<template>

    <link href="./src/assets/css/album.css" rel="stylesheet">
    <link href="./src/assets/css/pricing.css" rel="stylesheet">

    <loader v-if="isLoading"></loader>
    <div style="height:100%;">
        <headx></headx>
        <div class="row page0">

            <asidex @task-completed="onTaskCompleted"></asidex>

            <div class="cty col">
                <router-view></router-view>
            </div>
        </div>
    </div>
    <toast v-if="if_message" :message="message" :time="currentTime" />
</template>

<script>
import asidex from '@/components/main/aside.vue';
import headx from '@/components/main/head.vue';
import loader from "@/components/main/loader.vue";
import toast from "@/components/main/toast.vue";
import { ElNotification } from 'element-plus';
export default{
    name: "main",
    components: {
        asidex,
        headx,
        loader,
        toast,
    },
    data() {
        return {
            if_message: false,
            isLoading: false, // 控制加载效果组件的显示与否  
            currentTime: '',
        }
    },
    methods: {
        onTaskCompleted() {
            this.isLoading = false; // 任务完成后隐藏加载效果  
        },
        async fetchData() {
            this.isLoading = true; // 启动加载效果  
            try {
                await new Promise(resolve => setTimeout(resolve, 1000)); // 模拟耗时操作，如 API 请求  
            } catch (error) {
                console.error('Error fetching data:', error);
            }/*  finally {
                this.onTaskCompleted(); // 任务完成，隐藏加载效果  
            } */
        },
        handleMessage({ message, ifMessage }) {
            this.message = message;
            this.if_message = ifMessage;
            this.currentTime = this.formatTime(new Date());

            // 设置定时器，3秒后隐藏气泡  
            setTimeout(() => {
                this.if_message = false;
            }, 3000);
        },
        formatTime(date) {
            const hours = date.getHours();
            const minutes = date.getMinutes();
            const ampm = hours >= 12 ? '下午' : '上午';
            const formattedHours = hours % 12 || 12; // 将12小时制转换为0时  
            const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
            return `${ampm} ${formattedHours}点${formattedMinutes}分`;
        },

    },
    mounted() {
        this.fetchData(); // 组件挂载时获取数据 
        const notificationMessage = this.$route.query.notification;

        if (notificationMessage) {
            // 显示通知  
            ElNotification({
                title: '系统消息',
                message: "欢迎，" + notificationMessage,
                type: 'success',
                position: 'bottom-right',
            });
            this.$router.replace({ name: this.$route.name });
        }  
    }
}

</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
body {
    height: 100vh;
    overflow: hidden;
}
</style>