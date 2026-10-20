import { defineStore } from "pinia";
import {ref, onBeforeMount} from 'vue';
import router from '@/router';
import axios from 'axios';
import Cookies from "js-cookie";

const useProfileStore = defineStore('profileStore', () => {

    const isAuthenticated = ref(false);
    const isSuperUser = ref(false)
    const userName = ref(null);
    const id = ref(-1)
    
    async function fetchMe() {
        const r = await axios.get("/api/profile/me/");
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        isAuthenticated.value = r.data.is_authenticated;
        isSuperUser.value = r.data.is_superuser
        id.value = r.data.id;
        userName.value = r.data.is_authenticated ? r.data.username : null;
    }

    async function register(username, password) {
        const r = await axios.post('/api/profile/register/', {
            username: username,
            password: password,
        })
        fetchMe();
    }

    async function login(username, password) {
        const r = await axios.post('/api/profile/login/', {
            username: username,
            password: password,
        })
        fetchMe();
    }

    async function logout() {
        await axios.post("/api/profile/logout/")
        fetchMe();
    }

    onBeforeMount(() => {
        fetchMe();
    })

    return {
        isAuthenticated,
        userName,
        isSuperUser,
        id,

        fetchMe,
        login,
        logout,
        register
    }
})

export default useProfileStore;