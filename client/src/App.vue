<script setup>
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
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
        </ul>

        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Пользователь
            </a>
            <ul class=" dropdown-menu">
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </nav>
  </div>

  <div class="container">
    <router-view />
  </div>
</template>

<style scoped></style>