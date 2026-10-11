<script setup>
</script>

<template>
    <div class="objects">
        <div class="register">
            <span>Вы уже есть у нас в системе?</span>
            <router-link to="/login" type="button" class="btn btn-info"> Войдите в учетную запись</router-link>
        </div>
        <div class="register">
            <span>У вас нет учетной записи?</span>
            <router-link to="/register" type="button" class="btn btn-info"> Зарегестрируйтесь</router-link>
        </div>
    </div>
</template>