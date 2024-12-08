import { defineStore } from 'pinia';
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';

const authStructure = {
    coachId: null,
    firstName: '',
    lastName: '',
    email: '',
    token: null,
};

export const useAuthStore = defineStore('auth', {
    state: () => ({
        coach: { ...authStructure }
    }),
    actions: {
        async login(email, password) {
            try {
                const response = await axios.post('/login', { email:email, password: password });
                this.coach.coachId = response.data.id
                this.coach.firstName = response.data.first_name
                this.coach.lastName = response.data.last_name
                this.coach.email = response.data.email
                this.coach.token = response.data.access_token
                axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
            } catch (error) {
                console.error('Failed to login:', error);
                throw error;
            }
        },
        logout() {
            this.coach.coachId = null;
            this.coach.firstName = '';
            this.coach.lastName = '';
            this.coach.email = '';
            this.coach.token = null;
            delete axios.defaults.headers.common['Authorization'];
        },
    },
    persist: true,
});