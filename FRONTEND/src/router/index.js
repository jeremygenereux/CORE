import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../components/Landing.vue'
import Team from '../components/Team.vue'
import Dashboard from '../components/Dashboard.vue'
import Lines from '../components/Lines.vue'
import Signup from "@/components/Signup.vue";
import TeamSelect from "@/components/TeamSelect.vue";
import { useAuthStore } from "@/stores/auth.js";

const routes = [
    { path: '/', component: Landing },
    { path: '/teamSelect', component: TeamSelect, meta: { requiresAuth: true } },
    { path: '/team', component: Team, meta: { requiresAuth: true } },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/lines', component: Lines, meta: { requiresAuth: true } },
    { path: '/signup', component: Signup }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.coach.token) {
        console.warn('User is not authenticated, redirecting to login');
        next('/');
    } else {
        next();
    }
});

export default router