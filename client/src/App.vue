<script setup>
import NavBar from '@/components/NavBar.vue'
import ErrorModal from '@/components/ErrorModal.vue';
import useErrorStore from './stores/errorStore';
import { storeToRefs } from 'pinia';

const errorStore = useErrorStore()
const {
  textOfError,
  isError,
} = storeToRefs(errorStore)

</script>

<template>
  <nav-bar></nav-bar>

  <div class="container">
    <router-view />
  </div>

  <ErrorModal v-if="isError" v-model="isError" :textOfError="textOfError" />
</template>