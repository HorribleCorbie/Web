<script setup>
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';

const props = defineProps({
    needPrice: {
        type: Boolean,
        required: false,
        default: true
    }
})

const { role } = storeToRefs(useProfileStore())

const selectedNumber = defineModel('number', { default: null })
const selectedInDate = defineModel('in_date', { default: null })
const selectedOutDate = defineModel('out_date', { default: null })
const selectedClient = defineModel('client', { default: null })
const selectedPrice = defineModel('price', { default: null })


function clearNumber() {
    selectedNumber.value = null
}

function clearPrice() {
    selectedPrice.value = null
}

function clearInDate() {
    selectedInDate.value = null
}

function clearOutDate() {
    selectedOutDate.value = null
}

function clearClient() {
    selectedClient.value = null
}

function clearAll() {
    clearPrice()
    clearNumber()
    clearInDate()
    clearOutDate()
    clearClient()
}

</script>
<template>

    <div class="search-div">
        <div class="input-group">
            <input type="number" v-model="selectedNumber" class="form-control" placeholder="Найти номер..." min="1" />
            <button v-if="selectedNumber !== null" class="btn btn-outline-secondary" type="button"
                @click="clearNumber">✕</button>
        </div>

        <div class="input-group">
            <input type="date" v-model="selectedInDate" class="form-control"
                placeholder="Найти по дате заселения и позже..." />
            <button v-if="selectedInDate !== null" class="btn btn-outline-secondary" type="button"
                @click="clearInDate">✕</button>
        </div>

        <div class="input-group">
            <input type="date" v-model="selectedOutDate" class="form-control"
                placeholder="Найти по дате выселения и раньше..." />
            <button v-if="selectedOutDate !== null" class="btn btn-outline-secondary" type="button"
                @click="clearOutDate">✕</button>
        </div>

        <div v-if="needPrice" class="input-group">
            <input type="number" v-model="selectedPrice" class="form-control" placeholder="Найти по цене и ниже..."
                min="1" />
            <button v-if="selectedPrice !== null" class="btn btn-outline-secondary" type="button"
                @click="clearPrice">✕</button>
        </div>

        <div v-if="role!=2" class="input-group">
            <input type="text" v-model="selectedClient" class="form-control" placeholder="Найти по клиенту..."
                 />
            <button v-if="selectedClient !== null" class="btn btn-outline-secondary" type="button"
                @click="clearClient">✕</button>
        </div>

        <button class="btn btn-danger" type="button" @click="clearAll">✕</button>
    </div>

</template>