<script setup>
import { onBeforeMount, ref, computed } from 'vue'
import axios from 'axios'

const selectedAuthor = defineModel({ default: null })

const authors = ref([])
const searchQuery = ref('')
const isOpen = ref(false)

const label = a => a.first_name || a.username

const filteredAuthors = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return authors.value
  return authors.value.filter(a => label(a).toLowerCase().includes(q))
})

function selectAuthor(a) {
  selectedAuthor.value = a.id
  searchQuery.value = label(a)
  isOpen.value = false
}

function clearAuthor() {
  selectedAuthor.value = null
  searchQuery.value = ''
}

function onInput() {
  if (selectedAuthor.value !== null) selectedAuthor.value = null
}

const props = defineProps({
    type: {
        type: String,
        required: true
    }
})

onBeforeMount(async () => {
  const r = await axios.get(`/api/${props.type}/authors/`);
  authors.value = r.data
})
</script>

<template>
  <div class="search-div position-relative">
    <div class="input-group">
      <input type="text" v-model="searchQuery" class="form-control" placeholder="Выберите или введите автора..."
        @focus="isOpen = true" @blur="isOpen = false" @input="onInput" />
      <button v-if="selectedAuthor !== null" class="btn btn-outline-secondary" type="button"
        @click="clearAuthor">✕</button>
    </div>

    <ul v-if="isOpen" class="dropdown-menu show w-100" style="max-height: 200px; overflow-y: auto; z-index: 1000;">
      <li v-if="filteredAuthors.length === 0">
        <span class="dropdown-item text-muted">Ничего не найдено</span>
      </li>
      <li v-for="a in filteredAuthors" :key="a.id" @mousedown.prevent="selectAuthor(a)">
        <button type="button" class="dropdown-item">{{ label(a) }}</button>
      </li>
    </ul>
  </div>
</template>