<script setup>
import axios from 'axios';
import { onBeforeMount, ref, onMounted, watch } from 'vue';
import Cookies from 'js-cookie';
import SearchFilters from '@/components/SearchFilters.vue'
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';
import CreateProvision from '@/components/CreateProvision.vue';
import CreateStatistics from '@/components/CreateStatistics.vue';

let provisionModal = ref(false)


const profileStore = useProfileStore();
const {
  isSuperUser,
  id,
  thisCanBeAddAndChanged,
  role,
  userName
} = storeToRefs(profileStore)

const activeAccomodattions = ref([])
const clients = ref([])
const employees = ref([])

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

function clearServiceForm() {
  serviceToAdd.value = {
    name: '',
    price: ''
  }

  serviceAddPictureURL.value = ''

  if (serviceAddPicture.value) {
    serviceAddPicture.value.value = ''
  }
}

function clearEditServiceForm() {
  serviceToEdit.value = {
    name: '',
    price: ''
  }

  serviceUpdatePictureURL.value = ''

  if (serviceUpdatePicture.value) {
    serviceUpdatePicture.value.value = ''
  }
}

const isFormStats = ref(false)

window.onload = function () {
   const serviceModel = document.getElementById('serviceModel')

  serviceModel?.addEventListener('hidden.bs.modal', clearServiceForm)

  const editServiceModel = document.getElementById('editServiceModel')

  editServiceModel?.addEventListener('hidden.bs.modal', clearEditServiceForm)

  const statsModal = document.getElementById('statsModal')

  statsModal.addEventListener('hidden.bs.modal', function () {
    isFormStats.value = false
  })
}

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
  clearEditServiceForm()
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
  clearServiceForm()
  await fetchServices();
}


async function fetchAccomodattion() {
  const s = await axios.get("/api/accomodattion/", { params: { actual: 1, all: 1 } })
  activeAccomodattions.value = s.data
}

async function fetchEmployees() {
  const r = await axios.get("/api/users/?role=1", { params: { all: 1 } })
  employees.value = r?.data;
}

async function fetchClients() {
  const r = await axios.get("/api/users/?role=2", { params: { all: 1 } })
  clients.value = r.data;
}



onBeforeMount(async () => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  await fetchServices()
  await fetchAccomodattion()
  await fetchEmployees()
  await fetchClients()
})

async function onRemoveClick(service) {
  await axios.delete(`/api/service/${service.id}/`);
  await fetchServices();
}

const page = ref(1)
const pageItemsCount = ref(10)
const authorFilter = ref(null)

async function fetchServices() {
  loading.value = true
  const params = { page: page.value, page_size: pageItemsCount.value }
  if (authorFilter.value) params.user = authorFilter.value
  const r = await axios.get('/api/service/', { params })
  services.value = r.data.results
  pagesCount.value = Math.max(1, Math.ceil(r.data.count / pageItemsCount.value))
  loading.value = false
}

watch(authorFilter, () => {
  if (page.value === 1) fetchServices()
  else page.value = 1
})

const pagesCount = ref()

watch(page, () => {
  fetchServices();
})

function label(name) {
  return name.user_first_name ? name.user_first_name : name.user_name
}
</script>

<template>

  <div class="mycontainer">

    <div style="position:relative ">
      <h1>Услуги</h1>
      <button class="btn btn-info" v-if="isSuperUser" @click="isFormStats = true" style="position:absolute; top: 0; right: 0;" >
            <i class="bi bi-graph-up"></i>
      </button>
    </div>

    <div class="objects">
      <button type="button" v-if="thisCanBeAddAndChanged && role != 2" class="btn btn-warning" data-bs-toggle="modal"
        data-bs-target="#serviceModel">
        Добавить услугу
      </button>
      <div v-if="loading">Данные загружаются, подождите...</div>
      <div v-if="!loading && services.length == 0">У вас нет услуг</div>
      <search-filters v-if="isSuperUser" v-model="authorFilter" :type="'service'" />

      <table class="table">
        <thead>
          <tr>
            <th scope="col">Название</th>
            <th scope="col">Цена</th>
            <th scope="col">Фото</th>
            <th scope="col">Управление</th>
            <th v-if="isSuperUser" scope="col">Автор</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services">
            <td>{{ service.name }}</td>
            <td>{{ service.price }}</td>
            <td v-show="service.picture"><img :src="service.picture" type="button"
                @click="selectedImage = service.picture" data-bs-toggle="modal" data-bs-target="#imageModal"
                style="max-height: 60px;"></td>
            <td>
              <div class="buttons-div">
                <div class="buttons-div" v-if="(service.user === id || isSuperUser) && thisCanBeAddAndChanged">
                  <button class="btn btn-success" @click="onServiceEditClick(service)" data-bs-toggle="modal"
                    data-bs-target="#editServiceModal">
                    <i class="bi bi-pen-fill"> </i>
                  </button>
                  <button class="btn btn-danger" @click="selectedService = service" data-bs-toggle="modal"
                    data-bs-target="#deleteModal">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
                <button class="btn btn-warning" @click="selectedService = service; provisionModal = true">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </td>
            <td v-if="isSuperUser">{{ label(service) }}</td>
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

    <CreateProvision v-model="provisionModal" :services="[selectedService]" :accomodattions="activeAccomodattions"
      :clients="(thisCanBeAddAndChanged) ? clients : [{ id: id, username: userName }]"
      :employees="thisCanBeAddAndChanged ? employees : undefined" />

      <CreateStatistics v-if="isFormStats" v-model="isFormStats" :type="'service'"/>

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
