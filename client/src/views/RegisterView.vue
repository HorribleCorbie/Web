<template>
    <div class="mycontainer">
        <h1> Регистрация </h1>
        <form @submit.prevent="register">
            <div class="objects">
                <div>
                    <div class="form-floating">
                        <input v-model="username" class="form-control" id="username" type="text" required>
                        <label for="username"> Никнейм: </label>
                    </div>
                </div>
                <div>
                    <div class="form-floating">
                        <input v-model="password"  class="form-control"  id="password" type="password" required>
                        <label for="password"> Пароль: </label>
                    </div>
                </div>
                <button type="submit" class="btn btn-warning"> Регестрация </button>
            </div>
        </form>
        <div class="register">
            <span>Вы уже есть у нас в системе?</span>
            <a type="button" class="btn btn-info" href="/login"> Войдите в учетную запись</a>
        </div>
        <p v-if="error">
            {{ error }} </p>
        <p v-if="success">
            {{ success }} </p>
    </div>
</template>

<script>
import {
    getCSRFToken
} from '../stores/auth'

export default {
    data() {
        return {
            username: '',
            password: '',
            error: '',
            success: ''
        }
    },
    methods: {
        async register() {
            try {
                const response = await fetch(`/api/register/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    }),
                    credentials: 'include'
                })
                const data = await response.json()
                if (response.ok) {
                    this.success = 'Регистрация успешна.'
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 1000)
                } else {
                    this.error = data.error || 'Ошибка регистрации'
                }
            } catch (err) {
                this.error = 'Возникла ошибка в момент регистрации: ' + err
            }
        }
    }
} 
</script>