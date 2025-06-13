<template>

    <nav class="navbar shadow bg-dark navbar-dark navbar-expand-lg flex-colum head_nav" role="navigation">
        <div class="navbar-header">
            <router-link to="/" class="sd0"><img class="sd0" src="/sd0.png" alt="MK" height="70px">
            </router-link>
        </div>

        <ul class="navbar-nav collapse navbar-collapse">
            <li class="navbar-item">
                <router-link :to="{ name: 'home' }" class="p-2 a1" data-bs-toggle="tooltip" active-class="active">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor"
                        class="svg1 bi bi-house-door" viewBox="0 0 16 16">
                        <path
                            d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4z" />
                    </svg>&nbsp;首页
                </router-link>
            </li>
            <li class="navbar-item">
                <router-link :to="{ name: 'view' }" class="p-2 a1" data-bs-toggle="tooltip" active-class="active">
                    <svg class="svg1 bi bi-house-door" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                        fill="currentColor" viewBox="0 0 16 16">
                        <path
                            d="M2 10h3a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1m9-9h3a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-3a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1m0 9a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1zm0-10a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h3a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM2 9a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h3a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2zm7 2a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-3a2 2 0 0 1-2-2zM0 2a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm5.354.854a.5.5 0 1 0-.708-.708L3 3.793l-.646-.647a.5.5 0 1 0-.708.708l1 1a.5.5 0 0 0 .708 0z" />
                    </svg>&nbsp;审核</router-link>
            </li>

            <li class="navbar-item">
                <router-link :to="{ name: 'manage' }" class="p-2 a1" data-bs-toggle="tooltip" active-class="active">
                    <svg class="svg1 bi bi-kanban" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                        fill="currentColor" viewBox="0 0 16 16">
                        <path
                            d="M13.5 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zm-11-1a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z" />
                        <path
                            d="M6.5 3a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1zm-4 0a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1zm8 0a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1z" />
                    </svg>&nbsp;管理
                </router-link>
            </li>
            <li class="navbar-item">
                <router-link :to="{ name: 'cmt' }" class="p-2 a1" data-bs-toggle="tooltip" active-class="active">
                    <svg class="svg1 bi bi-envelope-plus" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                        fill="currentColor" viewBox="0 0 16 16">
                        <path
                            d="M2 2a2 2 0 0 0-2 2v8.01A2 2 0 0 0 2 14h5.5a.5.5 0 0 0 0-1H2a1 1 0 0 1-.966-.741l5.64-3.471L8 9.583l7-4.2V8.5a.5.5 0 0 0 1 0V4a2 2 0 0 0-2-2zm3.708 6.208L1 11.105V5.383zM1 4.217V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v.217l-7 4.2z" />
                        <path
                            d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-3.5-2a.5.5 0 0 0-.5.5v1h-1a.5.5 0 0 0 0 1h1v1a.5.5 0 0 0 1 0v-1h1a.5.5 0 0 0 0-1h-1v-1a.5.5 0 0 0-.5-.5" />
                    </svg>&nbsp;反馈
                </router-link>
            </li>

        </ul>

        <div class="navbar-right dropdown d-flex text-center">
            <nav class="text-right d-flex nav3">
                <input v-model="keyword" id="seracharea" class="form-control btnd" name="keyword" value='' required
                    type="text" maxlength="22" placeholder="搜索记录" aria-label="Search" :disabled="isDisabled">
                <p class="p1">&nbsp;</p>
                <button class="btn btn-outline-primary text-nowrap" type="submit" @click="sub"
                    :disabled="isDisabled"><strong>搜索</strong></button>
                <p class="p1">&nbsp;&nbsp;&nbsp;</p>


                <a href="#" class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
                    data-bs-toggle="dropdown" aria-expanded="false" id="dropdownMenuButton1">
                    <img title="用户" :src="`http://127.0.0.1:8000${avatar}`" alt="avatar" width="32" height="32"
                        class="rounded-circle me-2" />
                    <strong>{{ username }}</strong>
                </a>
                <ul class="dropdown-menu dropdown-menu-end text-center dropdown-menu-dark"
                    aria-labelledby="dropdownMenuButton1">

                    <li>
                        <router-link class="dropdown-item" :to="{ name: 'user', query: { token: userToken } }" target="_blank">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor"
                                class="person bi bi-person-circle" viewBox="0 0 16 16">
                                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                                <path fill-rule="evenodd"
                                    d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1" />
                            </svg>&nbsp;个人信息
                        </router-link>
                    </li>
                    <li>
                        <router-link class="dropdown-item" :to="{ name: 'register' }">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor"
                                class="person bi bi-person-fill-add" viewBox="0 0 16 16">
                                <path
                                    d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                                <path
                                    d="M2 13c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4" />
                            </svg>&nbsp;用户注册
                        </router-link>
                    </li>

                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li>
                        <router-link to="#" class="dropdown-item" @click.prevent="logout">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor"
                                class="person bi bi-person-exclamation" viewBox="0 0 16 16">
                                <path
                                    d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0M8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4m.256 7a4.5 4.5 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10q.39 0 .74.025c.226-.341.496-.65.804-.918Q8.844 9.002 8 9c-5 0-6 3-6 4s1 1 1 1z" />
                                <path
                                    d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-3.5-2a.5.5 0 0 0-.5.5v1.5a.5.5 0 0 0 1 0V11a.5.5 0 0 0-.5-.5m0 4a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1" />
                            </svg>&nbsp;注销登录
                        </router-link>
                    </li>
                </ul>
                <p class="p1">&nbsp;&nbsp;</p>

            </nav>
        </div>
    </nav>
</template>

<script>
import axios from 'axios';
export default {
    name: "head",
    data() {
        return {
            is_staff: false,
            username: '',
            avatar: '',
            isDisabled : false,
            keyword : '',
            userToken : sessionStorage.getItem('token'),
        }
    },

    methods: {
        logout() {
            // 清除存储在 sessionStorage 中的 token  
            sessionStorage.removeItem('token');
            // 跳转到登录页面  
            this.$router.push({ name: 'login', query: { notification: this.username } });
        },
        async get_user_info() {
            const token = sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/get_user_info', { token }, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = response.data;
                this.is_staff = data.is_staff;
                this.username = data.username;
                this.avatar = data.avatar;
            } catch (error) {
                console.error('获取用户信息时出错:', error); // 捕获并输出错误信息  
            }
        },
        async sub(){
            if (this.keyword.split(' ').join('').length != 0){
                this.$router.push({ name: "serach", query: { "keyword": this.keyword }});
                this.isDisabled = true;
                setTimeout(() => {
                    this.isDisabled = false; // 恢复状态  
                }, 1000); // 1秒后恢复 
            }
        },
    },
    mounted() {
        this.get_user_info(); // 组件挂载时获取数据  
    },

}
</script>