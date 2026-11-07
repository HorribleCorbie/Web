<script setup>
const selectedPrice = defineModel('price', { default: null })
const selectedQuantity = defineModel('quantity', { default: null })
const selectedName = defineModel('name', { default: null })


function clearName() {
    selectedName.value = null
}

function clearQuantity() {
    selectedQuantity.value = null
}

function clearPrice() {
    selectedPrice.value = null
}

function clearAll() {
    clearPrice()
    clearName()
    clearQuantity()
}

</script>
<template>

    <div class="search-div">
        <div class="input-group">
            <input type="text" v-model="selectedName" class="form-control" placeholder="Найти услугу..." />
            <button v-if="selectedName !== null" class="btn btn-outline-secondary" type="button"
                @click="clearName">✕</button>
        </div>

        <div class="input-group">
            <input type="number" v-model="selectedPrice" class="form-control" placeholder="Найти по цене и ниже..."
                min="1" />
            <button v-if="selectedPrice !== null" class="btn btn-outline-secondary" type="button"
                @click="clearPrice">✕</button>
        </div>

        <div class="input-group">
            <input type="number" v-model="selectedQuantity" class="form-control" placeholder="Найти по количеству"
                min="1" />
            <button v-if="selectedQuantity !== null" class="btn btn-outline-secondary" type="button"
                @click="clearQuantity">✕</button>
        </div>

        <button class="btn btn-danger" type="button" @click="clearAll">✕</button>
    </div>

</template>