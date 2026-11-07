<script setup>

const selectedName = defineModel('name', { default: null })
const selectedPrice = defineModel('price', { default: null })


function clearName() {
    selectedName.value = null
}

function clearPrice() {
    selectedPrice.value = null
}


function clearAll() {
    clearPrice()
    clearName()
}

</script>
<template>

    <div class="search-div">
        <div class="input-group">
            <input type="text" v-model="selectedName" class="form-control" placeholder="Найти номер..." min="1" />
            <button v-if="selectedName !== null" class="btn btn-outline-secondary" type="button"
                @click="clearName">✕</button>
        </div>

        <div class="input-group">
            <input type="number" v-model="selectedPrice" class="form-control" placeholder="Найти по цене и ниже..." min="1" />
            <button v-if="selectedPrice !== null" class="btn btn-outline-secondary" type="button"
                @click="clearPrice">✕</button>
        </div>

        <button class="btn btn-danger" type="button" @click="clearAll">✕</button>
    </div>

</template>