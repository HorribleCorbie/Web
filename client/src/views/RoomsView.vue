<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

const rooms = ref([])
let loading = ref(false)
const roomToAdd = ref({});
const roomToEdit = ref({});
let selectedRoom = ref()

async function onRoomEditClick(room) {
  roomToEdit.value = { ...room };
}

async function onUpdateRoom() {
  await axios.put(`/api/rooms/${roomToEdit.value.id}/`, {
    ...roomToEdit.value,
  });
  await fetchRooms();
}

async function onRoomAdd() {
  await axios.post("/api/rooms/", {
    ...roomToAdd.value,
  });
  await fetchRooms();
}

async function fetchRooms() {
  loading.value = true
  const r = await axios.get("/api/rooms/")
  rooms.value = r.data;
  loading.value = false
}


onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchRooms()
})

async function onRemoveClick(room) {
  await axios.delete(`/api/rooms/${room.id}/`);
  await fetchRooms();
}
</script>

<template>

  <div class="mycontainer">

    <h1>Номера отеля</h1>

    <div style="margin-bottom: 10px;">
      <form @submit.prevent.stop="onRoomAdd" class="objects">
        <div class="form-floating">
          <input type="number" class="form-control" min="1" v-model="roomToAdd.number" required />
          <label for="floatingInput">Номер</label>
        </div>
        <div class="form-floating">
          <input type="text" class="form-control" v-model="roomToAdd.description" required />
          <label for="floatingInput">Описание</label>
        </div>
        <div class="form-floating">
          <input type="number" min="1" class="form-control" v-model="roomToAdd.price" required />
          <label for="floatingInput">Цена</label>
        </div>
        <button class="btn btn-warning">
          Добавить
        </button>
      </form>
    </div>

    <div class="objects">
      <select class="form-select" v-model="selectedRoom">
        <option :value="room" v-for="room in rooms">
          Номер {{ room.number }}, цена: {{ room.price }}
        </option>
      </select>
      <button class="btn btn-success" @click="onRoomEditClick(selectedRoom)" data-bs-toggle="modal"
        data-bs-target="#editRoomModal">
        <i class="bi bi-pen-fill"> Редактировать</i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(selectedRoom)">
        <i class="bi bi-x"> Удалить номер</i>
      </button>
    </div>


    <div class="modal fade" id="editRoomModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Изменение номера
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects" >
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" v-model="roomToEdit.number" />
                  <label for="floatingInput">Номер</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" v-model="roomToEdit.price" />
                  <label for="floatingInput">Цена</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="roomToEdit.description" />
                <label for="floatingInput">Описание</label>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onUpdateRoom">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>

<style scoped>
.mycontainer {
  display: flex;
  flex-direction: column;

  margin: 40px auto;
  padding: 10px;
  max-width: 500px;

  border-radius: 15px;
  background-color: Snow;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

}

h1 {
  text-align: center;
}

.objects {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
