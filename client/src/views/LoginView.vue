<script setup>
import useProfileStore from '@/stores/profileStore';

import {ref} from 'vue';
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const {
    isAuthenticated,
    userName
} = storeToRefs(profileStore)


const username = ref("")
const password = ref("")

async function onLoginClick() {
    profileStore.login(username.value, password.value)
}

</script>

<template>
    <div class="mycontainer">
        <h1>Авторизация</h1>

        <form @submit.prevent.stop="onLoginClick">
            <div class="objects">
                <div>
                    <div class="form-floating">
                        <input v-model="username" required type="text" class="form-control" >
                        <label for="username">Никнейм:</label>
                    </div>
                </div>

                <div>
                    <div class="form-floating">
                         <input v-model="password" required type="password" class="form-control">
                        <label for="password">Пароль:</label>
                    </div>
                </div>
                <button class="btn btn-warning">
                    Войти в систему
                </button>
            </div>
            
        </form>
        <div class="register">
            <span>У вас нет учетной записи?</span>
            <a type="button" class="btn btn-info" href="/register"> Зарегестрируйтесь</a>
        </div>
    </div>
</template>