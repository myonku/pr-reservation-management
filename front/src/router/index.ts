import { createRouter, createWebHashHistory } from "vue-router";
import axios from "axios";

//
import login from "@/components/auth/login.vue"
import register from "@/components/auth/register.vue"
import reprovice from "@/components/auth/reprovice.vue"

//数据展示部分
import index from "@/components/home/index.vue"

//记录展示
import all_list from "@/components/resview/all_list.vue"
import apd_list from "@/components/resview/apd_list.vue"
import res_list from "@/components/resview/res_list.vue"
import serach from "@/components/resview/serach.vue"

//管理部分
import m_time from '@/components/elmanage/sep_manage.vue'
import m_device from '@/components/elmanage/device_manage.vue'

//意见反馈
import user_cmt from "@/components/comment/user_cmt.vue"
import stf_cmt from "@/components/comment/stf_cmt.vue"


//
import chome from "@/components/common/chome.vue"
import user from "@/components/common/user.vue"
import others from "@/components/common/others.vue"

const Placeholder = {
    template: '<router-view></router-view>'
};
const router = createRouter({
    
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            redirect: {name: "login"}
        },
        {
            name: "login",
            path: "/login",
            component: login
        },
        {
            name: "register",
            path: "/register",
            component: register
        },
        {
            name: "reprovice",
            path: "/reprovice",
            component: reprovice
        },
        {
            name: "cmain",
            path: "/cmain",
            component: () => import('@/components/common/cmain.vue'),
            redirect: { name: "chome" },
            meta: { requiresAuth: true},// 需要授权
            children: [
                {
                    path: "user",
                    name: "user",
                    component: user,
                    meta: { requiresAuth: true },
                },
                {
                    path: "chome",
                    name: "chome",
                    component: chome,
                    meta: { requiresAuth: true },
                },
                {
                    path: "others",
                    name: "others",
                    component: others,
                    meta: { requiresAuth: true },
                },
                { path: '', redirect: { name: 'chome' } }
            ]
        },
        {
            name: "main",
            path: '/main',
            component: () => import('@/components/main/main.vue'),
            redirect: { name: "home"},
            meta: { requiresAuth: true, requiresStaff: true } ,// 需要授权
            children: [
                {
                    path: "home",
                    name: "home",
                    component: Placeholder,
                    redirect: { name: "index" },
                    meta: { requiresAuth: true, requiresStaff: true },// 需要授权
                    children: [
                        { path: 'index', name: 'index', component: index },

                        { path: '', redirect: {name:'index'} } // 默认重定向到 index  
                    ]
                },
                {
                    path: 'view', // 管理部分的根路由  
                    name: 'view',
                    component: Placeholder, // 占位组件  
                    meta: { requiresAuth: true, requiresStaff: true },// 需要授权
                    redirect: { name: "res_list"},
                    children: [
                        { path: 'res_list', name: 'res_list', component: res_list },
                        { path: 'all_list', name: 'all_list', component: all_list },
                        { path: 'apd_list', name: 'apd_list', component: apd_list },
                        { path: 'serach', name: 'serach', component: serach },
                        { path: '', redirect: {name:'res_list'} } // 默认重定向到 res_list  
                    ]
                },
                {
                    path: 'manage', // 数据展示部分的根路由  
                    name: 'manage',
                    component: Placeholder, // 占位组件  
                    meta: { requiresAuth: true, requiresStaff: true },// 需要授权
                    redirect: { name: "m_time" },
                    children: [
                        { path: 'm_time', name: 'm_time', component: m_time },
                        { path: 'm_device', name: 'm_device', component: m_device },
               
                        { path: '', redirect: {name:'m_time'} } // 默认重定向到 m_time  
                    ]
                },
                {
                    path: "cmt",
                    name: "cmt",
                    component: Placeholder,
                    meta: { requiresAuth: true, requiresStaff: true },// 需要授权
                    redirect: { name: "user_cmt" },
                    children: [
                        {path: 'user_cmt', name: 'user_cmt', component: user_cmt},
                        { path: 'stf_cmt', name: 'stf_cmt', component: stf_cmt },
                        { path: '', redirect: { name: 'user_cmt' } }
                    ]
                },
                { path: '', redirect: {name:'index'} } // 默认重定向到home部分  
            ]
        },
        { path: '/:catchAll(.*)', redirect: '/main' } // 处理未知路由 
    ]
});


// 全局路由守卫  
router.beforeEach((to, from, next) => {
    const token = to.query.token || sessionStorage.getItem('token'); // 从 sessionStorage 中获取 token  
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!token) {
            next({ name: 'login' }); // 如果没有 token，重定向到登录页面  
        } else {
            // 这里可以添加验证 token 的逻辑  
            sessionStorage.setItem('token', token.toString()); // 存储 token  
            axios.post('http://127.0.0.1:8000/api/verify_token', { token })
                .then(response => {
                    const { valid, staff } = response.data;
                    // 判断需要的权限  
                    if (valid) {
                        // 检查是否需要 staff 权限  
                        if (to.matched.some(record => record.meta.requiresStaff)) {
                            if (staff) {
                                next(); // 如果 staff 为 true，放行  
                            } else {
                                next({ name: 'login' }); // 或者重定向到无权限页面  
                            }
                        } else {
                            next(); // 不需要 staff 的路由直接放行  
                        }
                    } else {
                        next({ name: 'login' }); // 验证失败，重定向到登录页面  
                    }  
                })
                .catch(() => {
                    next({ name: 'login' }); // 请求失败也重定向  
                });
        }
    } else {
        next(); // 不需要验证的路由直接放行  
    }
});
export default router