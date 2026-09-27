<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

const rooms = ref([])
let loading = ref(false)
const roomToAdd = ref({});
const roomToEdit = ref({});

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
  roomToAdd.value = { number: null, description: '', price: null };
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

    <div class="objects">
      <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#roomModel">
        Добавить номер
      </button>
      <div v-if="loading">Данные загружаются, подождите...</div>
      <div v-for="room in rooms">
        <div class="list">
          <div> Номер {{ room.number }}</div>
          <div> Цена: {{ room.price }}</div>
          <button class="btn btn-success" @click="onRoomEditClick(room)" data-bs-toggle="modal"
            data-bs-target="#editRoomModal">
            <i class="bi bi-pen-fill"> </i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(room)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
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
          <div class="modal-body objects">
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

    <div class="modal fade" id="roomModel" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Создание номера
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" min="1" v-model="roomToAdd.number" required />
                  <label for="floatingInput">Номер</label>
                </div>

              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" v-model="roomToAdd.price" required />
                  <label for="floatingInput">Цена</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="roomToAdd.description" required />
                  <label for="floatingInput">Описание</label>
                </div>

              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onRoomAdd">
              Добавить
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
  max-width: 1000px;

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

.list {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 10px;
  border-radius: 15px;
  background-color: white;
  padding: 5px;
  border: 1px solid silver;
  width: 100%;
  align-items: center;
}
</style>
