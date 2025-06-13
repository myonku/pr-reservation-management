<template>
    <link href="./src/assets/css/floating-labels.css" rel="stylesheet">
    <el-form class="form-rp">
        <div class="text-center mb-1">
            <img class="mb-4 img" src="/sd0.png" alt="" height="152">
            <h1 class="h2 mb-3 font-weight-normal"><strong>信息验证</strong></h1>
            <p><small>输入验证码以通过验证，同时重设你的账户密码</small></p>
            <p><small>若想要注册新账号，请<router-link class="tce" :to="{name: 'register'}">前往注册</router-link></small></p>
        </div>

        <el-form-item label="邮箱" prop="email" size="large" label-width="80" label-position="left">
            <el-input type="email" v-model="email" placeholder="请输入邮箱" ref="emailInput" />
        </el-form-item>

        <el-form-item label="验证码" prop="sc_password" :rules="passwordRules" label-position="left" label-width="80"
            size="large">
            <el-row style="width: 100%;">
                <el-col :span="16">
                    <el-input type="text" v-model="sc_password" placeholder="请输入验证码" ref="sc_password" show-password />
                </el-col>
                <el-col :span="8">
                    <div style="width: 100%;text-align: right;"><el-button type="primary">确定</el-button></div>
                </el-col>
            </el-row>

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
        <div class="form-group">
            <el-button class="btn btn-lg btn-primary btn-block" type="primary">XXXXX</el-button>
        </div>
        <p class="mt-3 mb-3 text-muted text-center"><small>要更换登录账户，请<router-link class="tce"
                    :to="{name: 'login'}">前往登录</router-link>，有其他问题请联系管理员：kwkz19171010@gmail.com</small></p>
        <p class="mt-3 mb-3 text-muted text-center">© 2024 @MyonKu</p>
    </el-form>
</template>

<script>

export default{
    name:"reprovice"
}
</script>

<style>
.form-rp{
    width: 480px;
        /* 根据需要调整 */
    margin: auto;
}
</style>