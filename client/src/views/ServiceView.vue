<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import Cookies from 'js-cookie';

const services = ref([])
let loading = ref(false)
const serviceToAdd = ref({});
const serviceToEdit = ref({});
let selectedService = ref()

async function onServiceEditClick(service) {
  serviceToEdit.value = { ...service };
}

async function onUpdateService() {
  await axios.put(`/api/service/${serviceToEdit.value.id}/`, {
    ...serviceToEdit.value,
  });
  await fetchServices();
}

async function onServiceAdd() {
  await axios.post("/api/service/", {
    ...serviceToAdd.value,
  });
  serviceToAdd = { name: '', price: null }
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
          <button class="btn btn-success" @click="onServiceEditClick(service)" data-bs-toggle="modal"
            data-bs-target="#editServiceModal">
            <i class="bi bi-pen-fill"> </i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(service)">
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
