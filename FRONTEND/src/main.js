import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './index.css';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VueApexCharts from "vue3-apexcharts";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)

app.use(pinia);
app.use(router);
app.use(VueApexCharts);
app.mount('#app');
