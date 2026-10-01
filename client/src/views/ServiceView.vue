<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

const services = ref([])
let loading = ref(false)
const selectedService = ref([])
const serviceToAdd = ref({});
const serviceToEdit = ref({});
let selectedImage = ref()

const serviceAddPicture = ref()
const serviceUpdatePicture = ref()

const serviceUpdatePictureURL = ref()
const serviceAddPictureURL = ref()

async function serviceAddPictureChange() {
  serviceAddPictureURL.value = URL.createObjectURL(serviceAddPicture.value.files[0])
}

async function serviceUpdatePictureChange() {
  serviceUpdatePictureURL.value = URL.createObjectURL(serviceUpdatePicture.value.files[0])
}

async function onServiceEditClick(service) {
  serviceToEdit.value = { ...service };
}

async function onUpdateService() {
  const formData = new FormData()
  if (serviceUpdatePicture.value.files[0]) {
    formData.append('picture', serviceUpdatePicture.value.files[0])
  }

  formData.set('name', serviceToEdit.value.name)
  formData.set('price', serviceToEdit.value.price)

  await axios.put(`/api/service/${serviceToEdit.value.id}/`, formData);
  serviceToEdit.value = {}
  serviceUpdatePicture.value.value = ''
  serviceAddPictureURL.value = undefined
  await fetchServices();
}

async function onServiceAdd() {
  const formData = new FormData()

  formData.append('picture', serviceAddPicture.value.files[0])
  formData.set('name', serviceToAdd.value.name)
  formData.set('price', serviceToAdd.value.price)

  await axios.post("/api/service/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }
  );
  serviceToAdd.value = {}
  serviceAddPicture.value.value = ''
  serviceAddPictureURL.value = undefined
  await fetchServices();
}

async function fetchServices() {
  loading.value = true
  const r = await axios.get("/api/service/")
  services.value = r.data;
  loading.value = false
}


onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchServices()
})

async function onRemoveClick(service) {
  await axios.delete(`/api/service/${service.id}/`);
  await fetchServices();
}
</script>

<template>

  <div class="mycontainer">

    <h1>Услуги</h1>

    <div class="objects">
      <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#serviceModel">
        Добавить услугу
      </button>
      <div v-if="loading">Данные загружаются, подождите...</div>
      <div v-for="service in services">
        <div class="list">
          <div> {{ service.name }}</div>
          <div v-show="service.picture"><img :src="service.picture" type="button"
              @click="selectedImage = service.picture" data-bs-toggle="modal" data-bs-target="#imageModal"
              style="max-height: 60px;"></div>
          <button class="btn btn-success" @click="onServiceEditClick(service)" data-bs-toggle="modal"
            data-bs-target="#editServiceModal">
            <i class="bi bi-pen-fill"> </i>
          </button>
          <button class="btn btn-danger" @click="selectedService = service" data-bs-toggle="modal"
            data-bs-target="#deleteModal">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editServiceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Изменение услуги
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="serviceToEdit.name" />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" v-model="serviceToEdit.price" />
                  <label for="floatingInput">Цена</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <input class="form-control" type="file" ref="serviceUpdatePicture" @change="serviceUpdatePictureChange">
              </div>
              <div class="col-auto">
                <img :src="serviceUpdatePictureURL || serviceToEdit.picture" style="max-height: 60px;">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onUpdateService">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>


    <div class="modal fade" id="serviceModel" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">
              Добавление услуги
            </h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body objects">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="serviceToAdd.name" />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" min="1" class="form-control" v-model="serviceToAdd.price" />
                  <label for="floatingInput">Цена</label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <input class="form-control" type="file" ref="serviceAddPicture" @change="serviceAddPictureChange">
              </div>
              <div class="col-auto">
                <img :src="serviceAddPictureURL" style="max-height: 60px;">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onServiceAdd">
              Сохранить
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
            <img :src="selectedImage">
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
                Вы точно хотите удалить услугу {{ selectedService.name }}?
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-danger"
              @click="onRemoveClick(selectedService)">
              Удалить
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>

<style scoped></style>
