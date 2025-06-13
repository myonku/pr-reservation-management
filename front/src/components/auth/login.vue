<template>

    <el-form class="form-signin" style="margin-top: 30px;" v-on:submit.prevent="login" ref="registrationForm">
        <div class="text-center mb-1">
            <el-image class="mb-4 img" src="/sd0.png" alt="" height="152" />
            <h1 class="h2 mb-3 font-weight-normal"><strong>欢迎！</strong></h1>
            <p><small>门禁通过预约申请需要注册后提交，若您是公司内部管理人员，则需要向管理员申请员工账户。</small></p>
            <p><small>若还没有账号，请<router-link class="tce" to="/register">前往注册</router-link></small></p>
        </div>

        <el-form-item label="用户名" prop="user" :rules="usernameRules" label-position="left" label-width="60"
            size="large">
            <el-input v-model="user" placeholder="请输入用户名" ref="usernameInput" />
        </el-form-item>

        <el-form-item label="密码" prop="pass" :rules="passwordRules" label-position="left" label-width="60" size="large">
            <el-input type="password" v-model="pass" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-form-item>
            <div style="width: 100%; text-align: right">
                <el-checkbox v-model="rememberMe">记住密码</el-checkbox>
            </div>
        </el-form-item>

        <el-form-item style="margin-left: 0px;">
            <div style="text-align: center; width: 100%;">
                <el-button type="primary" @click="login">登录</el-button>
            </div>
        </el-form-item>

        <p class="mt-3 mb-3 text-muted text-center"><small>若忘记账户密码，请<router-link class="tce"
                    :to="{ name: 'reprovice' }">前往验证</router-link>，或联系管理员：kwkz19171010@gmail.com</small></p>
        <p class="mt-3 mb-3 text-muted text-center" v-loading.fullscreen.lock="this.fullscreenLoading">© 2024 @MyonKu</p>
    </el-form>
</template>

<script>
import { ElForm, ElFormItem, ElInput, ElButton, ElCheckbox } from 'element-plus';
import axios from 'axios';
import { ElNotification } from 'element-plus'
export default {
    components: {
        ElForm,
        ElFormItem,
        ElInput,
        ElButton,
        ElCheckbox
    },
    data() {
        return {
            user: localStorage.getItem('user') || '', // 从 localStorage 获取用户名  
            pass: localStorage.getItem('pass') || '', // 从 localStorage 获取密码  
            rememberMe: !!(localStorage.getItem('user') && localStorage.getItem('pass')), // 根据是否有存储的值设置复选框状态  
            error: '',
            usernameRules: [
                { validator: this.checkUsernameAvailability, trigger: 'blur' },
            ],
            passwordRules: [
                { validator: this.PasswordValidator, trigger: 'blur' },
            ],
            fullscreenLoading : false
        };
    },
    mounted() {
        // 在页面加载后自动焦点输入框  
        this.$refs.usernameInput.focus();
        const notificationMessage = this.$route.query.notification;
        if (notificationMessage) {
            // 显示通知  
            ElNotification({
                title: '系统消息',
                message: "用户 " + notificationMessage + " 的登录信息已被注销",
                type: 'info',
                position: 'bottom-right',
            });
            this.$router.replace({ name: this.$route.name });
        }  
    },  
    methods: {
        async checkUsernameAvailability(rule, value, callback) {
            // 校验用户名长度  
            if (this.user.length < 3 || this.user.length > 12) {
                callback(new Error('用户名长度应在3到12个字符'));
            } else {
                callback();
            }
        },
        async PasswordValidator(rule, value, callback) {
            if (this.pass.length < 8 || this.pass.length > 16) {
                callback(new Error('密码长度应在8到16个字符'));
            } else {
                callback();
            }
        },
        handleCheckboxChange() {
            // 当复选框状态改变时更新 localStorage  
            if (this.rememberMe) {
                localStorage.setItem('user', this.user);
                localStorage.setItem('pass', this.pass);
            } else {
                localStorage.removeItem('user');
                localStorage.removeItem('pass');
            }
        },
        async login() {
            this.fullscreenLoading = true; // 显示加载状态  
            const valid = (this.user.length >= 3 && this.user.length <= 12 && this.pass.length >= 8 || this.pass.length <= 16);
            if (!valid) {
                this.fullscreenLoading = false; 
                ElNotification({
                    title: '检查错误',
                    message: '有一些字段似乎没有被正确填写，请检查后再试',
                    type: 'error',
                    position: 'bottom-right',
                })
                return;
            }
            this.handleCheckboxChange();
            // 提交表单后的处理逻辑  
            try {
                let params = new URLSearchParams();
                params.append("username", this.user);
                params.append("password", this.pass);

                const response = await axios.post('http://127.0.0.1:8000/api/v_login', params);
                // 存储 token 到 sessionStorage  
                this.fullscreenLoading = false;
                if (response.data.key === 0) {
                    this.$router.push({ name: 'home', query: { notification: this.user } }); // 登录成功后重定向到主页  
                    sessionStorage.setItem('token', response.data.token);
                } else if (response.data.key === 1) {
                    this.$router.push({ name: 'cmain', query: { notification: this.user } }); // 登录成功后重定向到主页  
                    sessionStorage.setItem('token', response.data.token);
                } else if (response.data.key === 10) {
                    ElNotification({
                        title: '验证错误',
                        message: '密码与用户名不匹配，请检查后再试',
                        type: 'error',
                        position: 'bottom-right',
                    })
                }
            } catch (error) {
                this.fullscreenLoading = false;
                ElNotification({
                    title: '登录失败',
                    message: '系统出现了一点小问题，请稍后再试',
                    type: 'error',
                    position: 'bottom-right',
                }) // 登录失败  
            }
        },
    },
};  
</script>

<style>
/* 你可以在这里添加自定义样式 */
.form-signin {
    max-width: 480px;
    /* 根据需要调整 */
    margin: auto;
}

.text-center {
    text-align: center;
}
</style>