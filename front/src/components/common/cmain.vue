<template>
    <div style="height: 100%;width: 100%;overflow: hidden">

        <el-page-header @back="goBack">
            <template #content>
                <div class="flex items-center">
                    <el-image style="height: 32px;margin-right: 10px;" class="mr-3" src="/sd1.png" />
                </div>
            </template>
            <template #extra>
                <el-switch style="margin-right: 16px;" v-model="isDark" inline-prompt @change="customToggleDark">
                    <template #active-action>
                        <el-icon>
                            <Moon />
                        </el-icon>
                    </template>
                    <template #inactive-action>
                        <el-icon>
                            <Sunny />
                        </el-icon>
                    </template>
                </el-switch>
                <el-button style="" v-if="mobile" @click="drawer = true"><el-icon>
                        <Menu />
                    </el-icon>
                </el-button>
                <el-dropdown placement="bottom-end" style="margin-left: 10px;">
                    <el-avatar class="mr-3" :size="32" :src="`http://127.0.0.1:8000${currentAvatar}`" />
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item disabled>xxxxxxxxxx</el-dropdown-item>
                            <el-dropdown-item>
                                <div style="height: 100%;width: 100%;text-align: center;" @click="user">个人信息</div>
                            </el-dropdown-item>
                            <el-dropdown-item>
                                <div style="height: 100%;width: 100%;text-align: center;" @click="logout">退出登录</div>
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>

            </template>
        </el-page-header>

        <el-drawer v-if="mobile" v-model="drawer" title="" :with-header="false" direction="ltr" size="80%">
            <el-menu :default-active="thisroute" style="height: 80%;" :router="true">
                <el-menu-item index="1" :route="{ name: 'chome' }" @click="clickroute('1')">
                    <el-icon>
                        <HomeFilled />
                    </el-icon>
                    <template #title>主页</template>
                </el-menu-item>

                <el-menu-item index="2" :route="{ name: 'user' }" @click="clickroute('2')">
                    <el-icon>
                        <UserFilled />
                    </el-icon>
                    <template #title>个人</template>
                </el-menu-item>

                <el-menu-item index="3" :route="{ name: 'others' }" @click="clickroute('3')">
                    <el-icon>
                        <Setting />
                    </el-icon>
                    <template #title>其他</template>
                </el-menu-item>
            </el-menu>
        </el-drawer>

        <el-container style="height: 100%;margin-right: 6px">
            <!-- 左侧 -->
            <el-aside v-if="!mobile" :style="{ width: isCollapse ? '63.2px' : '200px' }" style="position: relative;">
                <el-menu :default-active="thisroute" class="el-menu-vertical-demo" :collapse="isCollapse"
                    :router="true">
                    <el-menu-item index="1" :route="{ name: 'chome' }" @click="clickroute('1')">
                        <el-icon>
                            <HomeFilled />
                        </el-icon>
                        <template #title>主页</template>
                    </el-menu-item>

                    <el-menu-item index="2" :route="{ name: 'user' }" @click="clickroute('2')">
                        <el-icon>
                            <UserFilled />
                        </el-icon>
                        <template #title>个人</template>
                    </el-menu-item>

                    <el-menu-item index="3" :route="{ name: 'others' }" @click="clickroute('3')">
                        <el-icon>
                            <Setting />
                        </el-icon>
                        <template #title>其他</template>
                    </el-menu-item>
                    <hr>
                    <el-menu-item @click="handleCollpase">
                        <el-icon>
                            <template v-if="!isCollapse">
                                <Fold />
                            </template>
                            <template v-else>
                                <Expand />
                            </template>
                        </el-icon>
                        <template #title>{{ isCollapse ? '展开' : '收起' }}</template>
                    </el-menu-item>
                </el-menu>
            </el-aside>

            <!-- 主体 -->
            <el-main :style="{ transition: '0.2s' }" style="overflow-y: auto;height: 100%;position: relative;">
                <router-view v-slot="{ Component }">
                    <component ref="msgchild" :is="Component" @update:info="handleInfoUpdate" @msgevent="send_confirm_msg"></component>
                </router-view> />
            </el-main>
        </el-container>

    </div>

</template>

<style>
@import 'element-plus/theme-chalk/dark/css-vars.css';

.el-drawer .drawer-content {
    overflow: hidden;
    /* 禁止滚动 */
}

.el-page-header {
    padding: 10px;
    margin-left: 12px;
    margin-right: 12px;
    border-bottom: 1px solid lightgray;
}

.el-drawer {
    height: 100%;
    overflow: hidden;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu {
    height: 100%;
}

.el-aside {
    transition: width 0.3s;
    /* 侧边栏宽度的过渡动画 */
    height: 100%;
    overflow: hidden;
}
</style>
<script setup>
import { ref, onMounted, watch, computed, onBeforeUnmount, nextTick } from "vue";
import { useDark } from "@vueuse/core";
import { useRoute, useRouter } from 'vue-router';
import { ElNotification, ElMessage } from 'element-plus';

const if_staff = ref(false);
const route = useRoute();
const router = useRouter();
const isDark = useDark();
const drawer = ref(false)
const mobile = ref(false)   //是否为小屏幕
const isCollapse = ref(false)    //调整侧边栏
const screenWidth = ref(window.innerWidth)
const currentAvatar = ref('')
const currentName = ref('')
//
const msgchild = ref()
const socket = ref(null)
//
const send_confirm_msg = async (typex) => {
    if (typex == 0 || typex === 3) {
        return;
    }else if(typex === 10){
        const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
        if (!token) {
            console.error("Token is required.");
            return;
        }

        sendMessage({ type: 11, token: token });
        return;
    }
    const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    if (!token) {
        console.error("Token is required.");
        return;
    }
    if (socket.value) {
        sendMessage({ type: 12, token: token, typex: typex })
    }

}
const connect = async () => {
    await nextTick(); // 确保 DOM 更新 
    try {
        socket.value = new WebSocket('ws://127.0.0.1:8000/ws/clientsocket/');
    } catch {
        ElMessage({
            message: '服务器ws连接失败',
            type: 'error',
            plain: true,
        })
    }

    socket.value.onopen = () => {
        const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
        if (!token) {
            console.error("Token is required.");
            return;
        }
        
        sendMessage({ type: 11, token: token });
    };

    socket.value.onmessage = (event) => {
        // 处理接收到的消息  
        const messageData = JSON.parse(event.data);
        if (msgchild.value && msgchild.value.updatemessage) {
            msgchild.value.updatemessage(messageData);
        }else{
            ElMessage({
                message: '有新的消息，请前往首页查看',
                type: 'warning',
                plain: true,
            })
        }
    }

    socket.value.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
    }

    socket.value.onerror = (error) => {
        ElMessage({
            message: '服务器ws连接失败',
            type: 'error',
            plain: true,
        });
        console.error('WebSocket error:', error);
    };
}
const sendMessage = async (message) => {
    if (socket.value) {
        socket.value.send(JSON.stringify(message));
    }
}
const disconnect = async () => {
    if (socket.value) {
        socket.value.close();
        socket.value = null;
    }
}

//
const handleResize = () => {
    screenWidth.value = window.innerWidth
}
const thisroute = computed(() => {
    if (route.name === 'chome') return '1';
    else if (route.name === 'user') return '2';
    else if (route.name === 'others') return '3';
    return ''; // 默认空，如果没有匹配的  
});
onMounted(() => {
    window.addEventListener("resize", handleResize)
    mobile.value = screenWidth.value < 992; // 根据尺寸初始化isMobile
    const notificationMessage = route.query.notification;
    getUserInfo();
    if (notificationMessage) {
        // 显示通知  
        ElNotification({
            title: '系统消息',
            message: "欢迎，" + notificationMessage,
            type: 'success',
            position: 'bottom-right',
        });

        // 清空查询参数  
        router.replace({ name: 'cmain' }); // 用 replace 方法以移除该查询参数  
    }
    connect();
})
onBeforeUnmount(()=>{
    disconnect();
})
//watch监听屏幕宽度的变化，进行侧边栏的收缩和展开

watch(screenWidth, (newValue, oldValue) => {
    if (newValue < 992) {
        mobile.value = true
    } else {
        mobile.value = false
    }
    // console.log("值发生了变更", newValue, oldValue, isCollapse.value)
})
const handleCollpase = () => {    //调整侧边导航
    isCollapse.value = !isCollapse.value;
}
const clickroute = (x) => {
    drawer.value = false;
    thisroute.value = x
}
const goBack = () => {
    if (window.history.length <= 1) {
        router.push({ name: 'chome' }); // 如果没有历史记录，则跳转到主页  
    } else {
        router.go(-1); // 否则回到上一个页面  
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
        currentName.value = data.username || "未知"; // 处理空值情况  
        currentAvatar.value = data.avatar || ""; // 处理空值情况  
        if_staff.value = data.if_staff;
    } catch (error) {
        console.error("Error:", error);
    }
};
const handleInfoUpdate = (newInfo) => {
    if(newInfo.update == 1){
        getUserInfo()
    }
};
const user = () => {
    router.push({ name: 'user'});
};
const logout = () => {
    // 清除存储在 sessionStorage 中的 token  
    sessionStorage.removeItem('token');
    // 跳转到登录页面  
    router.push({ name: 'login', query: { notification: currentName.value } });
};
</script>