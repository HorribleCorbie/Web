import { defineStore } from "pinia";
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import Cookies from "js-cookie";
import router from '@/router'; 

const useProfileStore = defineStore('profileStore', () => {

    const isAuthenticated = ref(false);
    const isSuperUser = ref(false)
    const userName = ref(null);
    const id = ref(-1)
    const role = ref(null)
    const otp_uri = ref(null)
    const isOtpReady = ref(false)

    async function fetchMe() {
        const r = await axios.get("/api/profile/me/");
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        isAuthenticated.value = r.data.is_authenticated;
        isSuperUser.value = r.data.is_superuser
        id.value = r.data.id;
        userName.value = r.data.is_authenticated ? r.data.username : null;
        role.value = r.data.role ? r.data.role : null
        otp_uri.value = r.data.otp_uri
        const o = await axios.get("/api/profile/otp-status/")
        isOtpReady.value = Boolean(o.data.otp_good)
    }

    async function register(username, password) {
        const r = await axios.post('/api/profile/register/', {
            username: username,
            password: password,
        })
        await fetchMe()
        router.push('/')
    }

    async function login(username, password) {
        const r = await axios.post('/api/profile/login/', {
            username: username,
            password: password,
        })
        await fetchMe();
        router.push('/')
    }

    const thisCanBeAddAndChanged = computed (() => {
        if (role.value != 2 && isOtpReady.value)
            return true
        else 
            return false
    })

    async function otp_login(code) {
        const r = await axios.post('/api/profile/otp-login/', {
            key: String(code).trim()
        })
        if (r.data.success) {
            isOtpReady.value = true
            return true
        }
        else
        {
            isOtpReady.value = false
            return false
        }

    }

    async function logout() {
        await axios.post("/api/profile/logout/")
        fetchMe();
        router.push('/login')
    }

    onBeforeMount(() => {
        fetchMe();
    })

    return {
        isAuthenticated,
        userName,
        isSuperUser,
        id,
        role,
        thisCanBeAddAndChanged,
        isOtpReady,
        otp_uri,

        fetchMe,
        login,
        logout,
        register,
        otp_login
    }
})

export default useProfileStore;