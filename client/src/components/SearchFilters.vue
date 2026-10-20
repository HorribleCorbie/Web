<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue';
import axios from 'axios';
const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const clients = ref([])

const emit = defineEmits(['update:filteredItems']);
let selectedAuthor = ref(-1)

const authors = computed(() => {
  return new Map(
    props.items.map(i => [
      clientLabel(i.user),
      i.user
    ])
  );
});

function clientLabel(id) {
  const c = clients.value.find(x => x.id === id);
  return c != undefined ? (c.first_name ? c.first_name : c.username) : id
}

async function fetchUsers() {
  const r = await axios.get("/api/users/")
  clients.value = r.data;
}

const filteredItems = computed(() => {

  if (selectedAuthor.value===-1)
    return props.items

  return props.items.filter(item => item.user ===selectedAuthor.value)
});

watch(
  filteredItems,
  value => emit('update:filteredItems', value),
  { immediate: true }
);


onBeforeMount(async () => {
  await fetchUsers()
})
</script>

<template>
  <div class="search-div">
    <div>
      <select v-model="selectedAuthor" class="form-select search"">
        <option selected  :value="-1">Выберите автора</option>
        <option v-for="[name, id] in authors" :key="id" :value="id">{{ name }}</option>
      </select>
    </div>
  </div>
</template>