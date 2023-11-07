import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

import App from './App.vue';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import "bootstrap-icons/font/bootstrap-icons.css";
import LandingPage from "./components/LandingPage.vue";
import Step1Questionnaire from "./components/Step1Questionnaire.vue";
import Step2PicWatch from "./components/Step2PicWatch.vue";
import Step3TextRead from "./components/Step3TextRead.vue";

const myRouter = createRouter({
    mode: 'history',
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'landing-page',
            component: LandingPage
        },
        {
            path: '/step1_questionnaire',
            name: 'step1-questionnaire',
            component: Step1Questionnaire,
        },
        {
            path: '/step2_picwatch',
            name: 'step2-picwatch',
            component: Step2PicWatch,
        },
        {
            path: '/step3_textread',
            name: 'step3-textread',
            component: Step3TextRead,
        },
    ]
})

const myApp = createApp(App)

myApp.use(myRouter)

myApp.mount('#app')

myApp.use(ElementPlus, {
    locale: zhCn,
})

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    myApp.component(key, component)
}
