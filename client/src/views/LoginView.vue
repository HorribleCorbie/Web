<template>
    <div class="mycontainer">
        <h1>Авторизация</h1>

        <form @submit.prevent="login">
            <div class="objects">
                <div>
                    <div class="form-floating">
                        <input class="form-control" v-model="username" id="username" type="text" required
                            @input="resetError">
                        <label for="username">Никнейм:</label>
                    </div>
                </div>

                <div>
                    <div class="form-floating">
                        <input class="form-control" v-model="password" id="password" type="password" required
                            @input="resetError">
                        <label for="password">Пароль:</label>
                    </div>
                </div>
                <button type="submit" class="btn btn-warning">
                    Войти в систему
                </button>
            </div>
            
        </form>
        <div class="register">
            <span>У вас нет учетной записи?</span>
            <a type="button" class="btn btn-info" href="/register"> Зарегестрируйтесь</a>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script>
import {
    useAuthStore
} from '../stores/auth'

export default {
    setup() {
        const authStore = useAuthStore()
        return {
            authStore
        }
    },
    data() {
        return {
            username: "",
            password: "",
            error: ""
        }
    },
    methods: {
        async login() {
            await this.authStore.login(this.username, this.password, this.$router)
            if (!this.authStore.isAuthenticated) {
                this.error = 'Login failed. Please check your credentials.'
            }
        },
        resetError() {
            this.error = ""
        }
    }
} </script>