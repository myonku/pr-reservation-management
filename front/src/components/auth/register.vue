<template>
    <el-form class="form-register" style="margin-top: 30px;" ref="registrationForm">
        <div class="text-center mb-1">
            <el-image class="mb-4 img" src="/sd0.png" alt="" height="152" />
            <h1 class="h2 mb-3 font-weight-normal"><strong>用户注册</strong></h1>
            <p><small>这是普通预约用户的注册界面，将仅提供预约功能。内部员工请向管理人员申请账户。</small></p>
            <p><small>若已有账号，可<router-link class="tce" to="/login">前往登录</router-link></small></p>
        </div>

        <el-form-item label="用户名" prop="username" :rules="usernameRules" label-position="left" label-width="80"
            size="large">
            <el-input type="text" v-model="username" placeholder="请输入用户名" ref="usernameInput" />
        </el-form-item>

        <el-form-item label="邮箱（可选）" prop="email" size="large">
            <el-input type="email" v-model="email" placeholder="请输入邮箱" ref="emailInput" />
        </el-form-item>

        <el-form-item label="密码" prop="password" :rules="passwordRules" label-position="left" label-width="80"
            size="large">
            <el-input type="password" v-model="password" placeholder="请输入密码" ref="passwordInput" show-password />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword" :rules="confirmPasswordRules" label-position="left"
            label-width="80" size="large">
            <el-input type="password" v-model="confirmPassword" placeholder="请确认密码" ref="confirmPasswordInput"
                show-password />
        </el-form-item>

        <el-form-item style="margin-left: 0px;">
            <div style="text-align: center; width: 100%;">
                <el-button type="primary" @click="register">注册</el-button>
            </div>
        </el-form-item>

        <p class="mt-3 mb-3 text-muted text-center"><small>若忘记账户密码，请<router-link class="tce"
                    :to="{ name: 'reprovice' }">前往验证</router-link>，或联系管理员：perl@gmail.com</small></p>
        <p class="mt-3 mb-3 text-muted text-center" v-loading.fullscreen.lock="this.fullscreenLoading">© 2024 @MyonKu</p>
    </el-form>
</template>

<style>
.form-register {
    width: 480px;
    margin: auto;
}

.text-center {
    text-align: center;
}
</style>

<script>
import axios from 'axios';
import { ElNotification } from 'element-plus'
export default {
    data() {
        return {
            fullscreenLoading: false,
            username: '',
            password: '',
            email: '',
            confirmPassword: '',
            usernameRules: [
                { validator: this.checkUsernameAvailability, trigger: 'blur' },
            ],
            passwordRules: [
                { validator: this.PasswordValidator, trigger: 'blur' },
            ],
            confirmPasswordRules: [
                { validator: this.confirmPasswordValidator, trigger: 'blur' },
            ],
        };
    },
    mounted() {
        // 在页面加载后自动焦点输入框  
        this.$refs.usernameInput.focus();
    },  
    methods: {

        async checkUsernameAvailability(rule, value, callback) {
            // 校验用户名长度  
            if (this.username.length < 3 || this.username.length > 12) {
                return callback(new Error('用户名长度应在3到12个字符'));
            }else{
                try {
                    let params = new URLSearchParams();
                    params.append("username", this.username);
                    const response = await axios.post('http://127.0.0.1:8000/api/username_validator', params);

                    const data = response.data.result;
                    if (data) {
                        callback(); // 用户名可用  
                    } else {
                        callback(new Error('用户名已被使用，请选择其他用户名')); // 用户名已存在  
                    }
                } catch (error) {
                    console.error("检查用户名可用性时出错:", error);
                    callback(new Error('无法检查用户名，请稍后重试')); // 请求出错，反馈用户  
                }
            }
            // 发起检查用户名可用性请求  
            
        },
        async PasswordValidator(rule, value, callback) {
            if (this.password.length === 0) {
                callback(new Error('密码不能为空'));
            }
            else if (this.password.length < 8 || this.password.length > 16) {
                callback(new Error('密码长度应在8到16个字符'));
            } else {
                callback();
            }
        },
        async confirmPasswordValidator(rule, value, callback) {
            if (this.confirmPassword.length === 0) {
                callback(new Error('确认密码不能为空'));
            }
            else if (this.confirmPassword !== this.password) {
                callback(new Error('确认密码与密码不匹配'));
            } else {
                callback();
            }
        },
        async register(){
            this.fullscreenLoading = true; // 显示加载状态 
            const valid = (this.username.length >= 3 && this.username.length <= 12 && this.password.length >= 8 && this.password.length <= 16);
            if (!valid){
                this.fullscreenLoading = false; 
                ElNotification({
                    title: '检查错误',
                    message: '有一些字段似乎没有被正确填写，请检查后再试',
                    type: 'error',
                    position: 'bottom-right',
                })
                return;
            } else{
                let params = new URLSearchParams();
                params.append("username", this.username);
                params.append("password", this.password);
                try{
                    const response = await axios.post('http://127.0.0.1:8000/api/v_register', params);
                    if (response.data.key === 0) {
                        this.fullscreenLoading = false; 
                        ElNotification({
                            title: '系统消息',
                            message: '注册成功！即将前往登录',
                            type: 'success',
                            position: 'bottom-right',
                        });
                        setTimeout(
                            () => {
                                this.$router.push({ name: 'login' });
                            }, 600
                        )
                    }
                } catch (err) {
                    this.fullscreenLoading = false; 
                    ElNotification({
                        title: '系统消息',
                        message: '注册失败，请稍后再试',
                        type: 'error',
                        position: 'bottom-right',
                    })
                }
                
            } 
        }
    },
};  
</script>
