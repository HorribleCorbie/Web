<script setup>
import useProfileStore from '../stores/profileStore';
import { storeToRefs } from 'pinia';


const profileStore = useProfileStore();
const {
    isAuthenticated,
    userName
} = storeToRefs(profileStore)


async function onLogoutButtonClick() {
    profileStore.logout();
}

</script>

<template>
    <div class="container">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-collapse justify-content-between" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item active">
                        <router-link class="nav-link" to="/">
                            Номерной фонд
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/service">
                            Услуги
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/accomodattion">
                            Проживание
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/provision">
                            Оказание услуги
                        </router-link>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Пользователь
                        </a>
                        <ul class=" dropdown-menu">
                            <li><a class="dropdown-item" href="/admin">Админка</a></li>
                        </ul>
                    </li>
                </ul>

                <div>
                    <button v-if="isAuthenticated" class="btn btn-outline-success" @click="onLogoutButtonClick">
                        Выйти из аккаунта {{ userName }}
                    </button>
                </div>

            </div>
        </nav>
    </div>
</template>