<script setup>
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

const rooms = ref([])
const selectedRoom = ref([])
let loading = ref(false)

const roomToAdd = ref({});
const roomToEdit = ref({});

const roomsPictureRef = ref([]);
const roomsEditPictureRef = ref([]);
const roomAddImageUrl = ref([])
const roomUpdateImageUrl = ref([])

const newDownloadedImages = ref({})

let currentImage = ref([])

async function roomsAddImageChange() {
  for (const file of roomsPictureRef.value.files) {
    roomAddImageUrl.value.push(URL.createObjectURL(file))
  }
}

async function roomsUpdateImageChange() {
  for (const file of roomsEditPictureRef.value.files) {
    const url = URL.createObjectURL(file)
    roomUpdateImageUrl.value.push(url)
    newDownloadedImages.value[file.name] = url
  }
}

async function onRoomEditClick(room) {
  roomToEdit.value = { ...room }
  for (const image of roomToEdit.value.picture) {
    roomUpdateImageUrl.value.push(image.picture)
  }
}

function closeAddModal() {
  roomAddImageUrl.value = []
  if (roomsPictureRef.value) roomsPictureRef.value.value = ''
  roomToAdd.value = { number: '', description: '', price: '' }
}

function closeUpdateModal() {
  roomUpdateImageUrl.value = []
  if (roomsEditPictureRef.value) roomsEditPictureRef.value.value = ''
  roomToEdit.value = { number: '', description: '', price: '' }
}

async function onUpdateRoom() {
  const formData = new FormData()


  if (roomsEditPictureRef.value.files) {
    for (const file of roomsEditPictureRef.value.files) {
      const name = file.name
      const currentImage = newDownloadedImages.value[name];

      if (roomUpdateImageUrl.value.includes(currentImage)) {
        formData.append('images', file)
      }
    }
  }

  formData.set('number', roomToEdit.value.number)
  formData.set('description', roomToEdit.value.description)
  formData.set('price', roomToEdit.value.price)

  for (const image of roomToEdit.value.picture) {
    if (!roomUpdateImageUrl.value.some(url => url == image.picture)) {
      formData.append('images_to_delete', image.id)
    }
  }

  await axios.put(`/api/rooms/${roomToEdit.value.id}/`, formData)
  closeUpdateModal()
  await fetchRooms();
}

async function onRoomAdd() {
  const formData = new FormData()

  formData.set('number', roomToAdd.value.number)
  formData.set('description', roomToAdd.value.description)
  formData.set('price', roomToAdd.value.price)

  for (const file of roomsPictureRef.value.files) {
    formData.append('images', file)
  }

  await axios.post("/api/rooms/", formData, {
    headers:
    {
      'Content-Type': 'multipart/form-data'
    }
  });
  closeAddModal()
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
          <div v-show="room.picture"><img :src="room.picture[0]?.picture" type="button"
              @click="currentImage = room.picture" data-bs-toggle="modal" data-bs-target="#imageModal"
              style="max-height: 60px;"></div>
          <button class="btn btn-success" @click="onRoomEditClick(room)" data-bs-toggle="modal"
            data-bs-target="#editRoomModal">
            <i class="bi bi-pen-fill"> </i>
          </button>
          <button class="btn btn-danger" @click="selectedRoom = room" data-bs-toggle="modal"
            data-bs-target="#deleteModal">
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
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="closeUpdateModal"></button>
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
            <div class="row">
              <div class="col">
                <input class="form-control" type="file" ref="roomsEditPictureRef" @change="roomsUpdateImageChange"
                  multiple>
              </div>
            </div>
            <div class="row output-images">
              <div v-for="image in roomUpdateImageUrl">
                <div style="position:relative">
                  <img :src="image" style="max-height: 60px">
                  <button class="btn btn-danger" style="position:absolute; padding: 0;width: 20px;height: 20px;  border-radius: 0; top: 0;  left: 0;  transform: translate(0%, 0%);  
                    -ms-transform: translate(0%, 0%);"
                    @click="roomUpdateImageUrl.splice(roomUpdateImageUrl.indexOf(image), 1);">
                    <i class="bi bi-x" style="display: flex; justify-content: center; align-items: center;"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="closeUpdateModal">
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
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="closeAddModal"></button>
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
            <div class="row">
              <div class="col">
                <input class="form-control" type="file" ref="roomsPictureRef" @change="roomsAddImageChange" multiple>
              </div>
            </div>
            <div class="row output-images">
              <div v-for="image in roomAddImageUrl">
                <img :src="image" style="max-height: 60px">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="closeAddModal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onRoomAdd">
              Добавить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects">
            <div id="carousel" class="carousel slide" data-ride="carousel">
              <div class="carousel-inner">
                <div class="carousel-item " v-for="(image, index) in currentImage" :class="{ active: index === 0 }">
                  <img class="d-block w-100" :src="image.picture" style="object-fit: contain; max-height: 500px;">
                </div>
              </div>
              <div v-if="currentImage.length > 1">
                <button class="carousel-control-prev" type="button" data-bs-target="#carousel" data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carousel" data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
          </div>
        </div>
      </div>
    </div>


    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Удаление
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects ">
            <div class="row">
              <div class="col">
                Вы точно хотите удалить номер {{ selectedRoom.number }}?
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-danger" @click="onRemoveClick(selectedRoom)">
              Удалить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
