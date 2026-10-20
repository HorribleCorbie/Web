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

async function onRegisterClick() {
    profileStore.register(username.value, password.value)
}
</script>
<template>
    <div class="mycontainer">
        <h1> Регистрация </h1>
        <form @submit.prevent.stop="onRegisterClick">
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
                    Зарегистрироваться
                </button>
            </div>
        </form>
        <div class="register">
            <span>Вы уже есть у нас в системе?</span>
            <a type="button" class="btn btn-info" href="/login"> Войдите в учетную запись</a>
        </div>
    </div>
</template>