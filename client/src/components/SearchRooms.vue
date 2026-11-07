<script setup>

const selectedNumber = defineModel('number', { default: null })
const selectedDescription = defineModel('description', { default: null })
const selectedPrice = defineModel('price', { default: null })


function clearNumber() {
    selectedNumber.value = null
}

function clearPrice() {
    selectedPrice.value = null
}

function clearDescription() {
    selectedDescription.value = null
}

function clearAll() {
    clearPrice()
    clearNumber()
    clearDescription()
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
            <input type="text" v-model="selectedDescription" class="form-control" placeholder="Найти по описанию..." />
            <button v-if="selectedDescription !== null" class="btn btn-outline-secondary" type="button"
                @click="clearDescription">✕</button>
        </div>

        <div class="input-group">
            <input type="number" v-model="selectedPrice" class="form-control" placeholder="Найти по цене и ниже..." min="1" />
            <button v-if="selectedPrice !== null" class="btn btn-outline-secondary" type="button"
                @click="clearPrice">✕</button>
        </div>

        <button class="btn btn-danger" type="button" @click="clearAll">✕</button>
    </div>

</template>