<script setup>
import axios from 'axios';
import { onBeforeMount, ref, toRaw, computed, watch } from 'vue';
import Cookies from 'js-cookie';
import SearchFilters from '@/components/SearchFilters.vue'
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';
import CreateAccommodattion from '@/components/CreateAccommodattion.vue';
import CreateStatistics from '@/components/CreateStatistics.vue';
import SearchRooms from '@/components/SearchRooms.vue';

const accomodattionModal = ref(false)

const profileStore = useProfileStore();
const {
  isSuperUser,
  id,
  thisCanBeAddAndChanged,
  userName,
  role
} = storeToRefs(profileStore)


const page = ref(1);
const pageItemsCount = ref(10);
const rooms = ref([])
const selectedRoom = ref([])
let loading = ref(false)
const clients = ref([])

const roomToAdd = ref({});
const roomToEdit = ref({});

const roomsPictureRef = ref([]);
const roomsEditPictureRef = ref([]);
const roomAddImageUrl = ref([])
const roomUpdateImageUrl = ref([])

const newDownloadedImages = ref({})
const selectedImages = ref([])

let currentImage = ref([])
const isFormStats = ref(false)

window.onload = function () {
  var myModal = document.getElementById('imageModal')

  myModal.addEventListener('hidden.bs.modal', function () {
    currentImage.value = []
  })

  var roomModal = document.getElementById('roomModel')

  roomModal.addEventListener('hidden.bs.modal', function () {
    closeAddModal()
  })
}

const isFormValid = computed(() => {
  if (!roomToAdd.value || Object.keys(roomToAdd.value).length === 0) {
    return false;
  }
  const { number, description, price } = roomToAdd.value;
  return (number && description && price);
});

async function roomsAddImageChange() {
  for (const file of roomsPictureRef.value.files) {
    const url = URL.createObjectURL(file)
    roomAddImageUrl.value.push(url)
    newDownloadedImages.value[file.name] = url
  }
  selectedImages.value = [...selectedImages.value, Array.from(roomsPictureRef.value.files)]
}

async function roomsUpdateImageChange() {
  for (const file of roomsEditPictureRef.value.files) {
    const url = URL.createObjectURL(file)
    roomUpdateImageUrl.value.push(url)
    newDownloadedImages.value[file.name] = url
  }
  selectedImages.value = [...selectedImages.value, Array.from(roomsEditPictureRef.value.files)]
}

async function onRoomEditClick(room) {
  roomToEdit.value = { ...room }
  for (const image of roomToEdit.value.picture) {
    roomUpdateImageUrl.value.push(image.picture)
  }
}

function closeAddModal() {
  newDownloadedImages.value = {}
  roomAddImageUrl.value = []
  if (selectedImages.value) selectedImages.value = ''
  if (roomsPictureRef.value) roomsPictureRef.value.value = ''
  roomToAdd.value = { number: '', description: '', price: '' }
}

function closeUpdateModal() {
  newDownloadedImages.value = {}
  currentImage.value = []
  roomUpdateImageUrl.value = []
  if (selectedImages.value) selectedImages.value = ''
  if (roomsEditPictureRef.value) roomsEditPictureRef.value.value = ''
  roomToEdit.value = { number: '', description: '', price: '' }
}

async function onUpdateRoom() {
  const formData = new FormData()
  if (selectedImages.value) {
    const filesArray = toRaw(selectedImages.value).flatMap(item => item.files ?? item)
    for (const file of filesArray) {
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
  formData.set('user', id.value)

  if (selectedImages.value) {
    const filesArray = toRaw(selectedImages.value).flatMap(item => item.files ?? item)
    for (const file of filesArray) {
      const name = file.name
      const currentImage = newDownloadedImages.value[name];

      if (roomAddImageUrl.value.includes(currentImage)) {
        formData.append('images', file)
      }
    }
  }

  await axios.post("/api/rooms/", formData);
  closeAddModal()
  await fetchRooms();
}

async function fetchAll(url, params = {}) {
  const r = await axios.get(url, { params: { ...params, all: 1 } })
  return Array.isArray(r.data) ? r.data : r.data.results
}

async function fetchClients() {
  clients.value = await fetchAll('/api/users/', { role: 2 })
}

const authorFilter = ref(null)
const numberFilter = ref(null)
const descriptionFilter = ref(null)
const priceFilter = ref(null)

async function fetchRooms() {
  loading.value = true
  const params = { page: page.value, page_size: pageItemsCount.value }
  if (authorFilter.value) params.user = authorFilter.value
  if (numberFilter.value) params.number = numberFilter.value
  if (descriptionFilter.value) params.description = descriptionFilter.value
  if (priceFilter.value) params.price = priceFilter.value
  const r = await axios.get('/api/rooms/', { params })
  rooms.value = r.data.results
  pagesCount.value = Math.max(1, Math.ceil(r.data.count / pageItemsCount.value))
  loading.value = false
}

watch([authorFilter, numberFilter, descriptionFilter, priceFilter], () => {
  if (page.value === 1) fetchRooms()
  else page.value = 1
})

const pagesCount = ref()

watch(page, () => {
  fetchRooms();
})

onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchRooms()
  await fetchClients()
})

async function onRemoveClick(room) {
  await axios.delete(`/api/rooms/${room.id}/`);
  await fetchRooms();
}

function label(name) {
  return name.user_first_name ? name.user_first_name : name.user_name
}

function exportExel() {
  axios({
    url: '/api/rooms/export',
    method: 'GET',
    responseType: 'blob',
  }).then((response) => {
    const href = URL.createObjectURL(response.data)

    const link = document.createElement('a');
    link.href = href;
    link.setAttribute('download', 'Report.xlsx'); 
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(href);
  });
}

</script>

<template>

  <div class="mycontainer">

    <div style="position:relative ">
      <h1>Номера отеля</h1>
      <button class="btn btn-info" v-if="isSuperUser" @click="isFormStats = true"
        style="position:absolute; top: 0; right: 0;">
        <i class="bi bi-graph-up"></i>
      </button>
      <button class="btn btn-info" v-if="isSuperUser" @click="exportExel()" style="position:absolute; top: 0; left: 0;">
        <i class="bi bi-arrow-down-square"></i>
      </button>
    </div>

    <div class="objects">
      <button type="button" v-if="thisCanBeAddAndChanged && role != 2" class="btn btn-warning" data-bs-toggle="modal"
        data-bs-target="#roomModel">
        Добавить номер
      </button>
      <div v-if="loading">Данные загружаются, подождите...</div>
      <search-filters v-if="isSuperUser" v-model="authorFilter" :type="'rooms'" />

      <SearchRooms v-model:number="numberFilter" v-model:description="descriptionFilter" v-model:price="priceFilter" />

      <div v-if="!loading && rooms.length == 0" style="text-align: center;">У вас нет комнат</div>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Номер</th>
            <th scope="col">Описание</th>
            <th scope="col">Фото</th>
            <th scope="col">Цена</th>
            <th scope="col">Управление</th>
            <th v-if="isSuperUser" scope="col">Автор</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="room in rooms">
            <th scope="row">{{ room.number }}</th>
            <td>{{ room.description }}</td>
            <td v-show="room.picture"><img :src="room.picture[0]?.picture" type="button"
                @click="currentImage = room.picture" data-bs-toggle="modal" data-bs-target="#imageModal"
                style="max-height: 60px;"></td>
            <td>{{ room.price }}</td>
            <td>
              <div class="buttons-div">
                <div class="buttons-div" v-if="(room.user === id || isSuperUser) && thisCanBeAddAndChanged">
                  <button class="btn btn-success" @click="onRoomEditClick(room)" data-bs-toggle="modal"
                    data-bs-target="#editRoomModal">
                    <i class="bi bi-pen-fill"> </i>
                  </button>
                  <button class="btn btn-danger" @click="selectedRoom = room" data-bs-toggle="modal"
                    data-bs-target="#deleteModal">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
                <button class="btn btn-warning" @click="selectedRoom = room; accomodattionModal = true">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </td>
            <td v-if="isSuperUser">{{ label(room) }}</td>
          </tr>
        </tbody>
      </table>

      <nav aria-label="Page navigation example">
        <ul class="pagination justify-content-center">
          <li class="page-item " v-if="page > 1" @click="page -= 1">
            <a class="page-link" href="#">Previous</a>
          </li>

          <li @click="page = page - 1" class="page-item" v-if="page - 1 > 0"><a class="page-link">{{ page - 1 }}</a>
          </li>
          <li class="page-item" v-if="page > 0"><span href="" class="page-link">{{ page }}</span></li>
          <li @click="page = page + 1" class="page-item" v-if="page + 1 < pagesCount"><a class="page-link">{{ page + 1
              }}</a></li>
          <li @click="page = page + 2" class="page-item" v-if="page + 2 < pagesCount"><a class="page-link">{{ page + 2
              }}</a></li>
          <li @click="page = page + 3" class="page-item" v-if="page + 3 < pagesCount"><a class="page-link">{{ page + 3
              }}</a></li>

          <li class="page-item" v-if="page < pagesCount">
            <a class="page-link" href="#" @click="page += 1">Next</a>
          </li>
        </ul>
      </nav>

    </div>


    <CreateAccommodattion v-if="accomodattionModal" v-model="accomodattionModal"
      :clients="(thisCanBeAddAndChanged) ? clients : [{ id: id, username: userName }]" :rooms="[selectedRoom]" />

    <CreateStatistics v-model="isFormStats" :type="'rooms'" />

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
                <div style="position:relative">
                  <img :src="image" style="max-height: 60px">
                  <button class="btn btn-danger" style="position:absolute; padding: 0;width: 20px;height: 20px;  border-radius: 0; top: 0;  left: 0;  transform: translate(0%, 0%);  
                    -ms-transform: translate(0%, 0%);"
                    @click="roomAddImageUrl.splice(roomAddImageUrl.indexOf(image), 1);">
                    <i class="bi bi-x" style="display: flex; justify-content: center; align-items: center;"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="closeAddModal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" :disabled="!isFormValid" type="button" class="btn btn-success"
              @click="onRoomAdd">
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
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="currentImage = []"></button>
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
