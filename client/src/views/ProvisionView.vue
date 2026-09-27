<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, } from 'vue';
import Cookies from 'js-cookie';

const provisionToAdd = ref({});
const provisionToEdit = ref({});

const provisions = ref([])
const accomodattions = ref([])
const clients = ref([])
const employees = ref([])
const services = ref([])

let loading = ref(false)
let isError = ref(false)
let textOfError = ref()


const source = computed(() => {
    return provisionToEdit.value.id
        ? provisionToEdit.value
        : provisionToAdd.value
})

const totalPrice = computed(() => {
    if (source.value.quantity != undefined && source.value.service) {
        const quantity = source.value.quantity
        const service = services.value.find(x => x.id === source.value.service)
        return quantity * service.price
    }
    return 0
});


function findCLient(id_accomodattion) {
    const accomodattion = findAccomodattion(id_accomodattion)
    if (accomodattion != undefined) {
        const client = clients.value.find(x => x.id === accomodattion.client)
        return client != undefined ? (client.first_name ? client.first_name : client.username) : id_accomodattion
    }
}

function accomodattionLabel(id) {
    const acc = findAccomodattion(id);
    if (acc != undefined) return `Клиент: ${findCLient(id)}, даты: ${acc.in_date} по ${acc.out_date}`;
}

function findAccomodattion(id_accomodattion) {
    const accomodattion = accomodattions.value.find(x => x.id === id_accomodattion)
    return accomodattion
}

function findService(id_service) {
    const s = services.value.find(x => x.id === id_service)
    return s ? s.name : id_service
}

async function onProvisionEditClick(provision) {
    provisionToEdit.value = { ...provision };
}

async function onUpdateProvision() {
    const payload = {
        ...provisionToEdit.value,
        price: totalPrice.value,
    };
    try {
        await axios.put(`/api/provision/${provisionToEdit.value.id}/`, payload);
        await fetchProvision();
        provisionToEdit.value = {}
    } catch (error) {
        console.log(error.response?.data);
        isError.value = true
        textOfError.value = error.response.data[0]
    }
}

async function onProvisionAdd() {
    const payload = {
        ...provisionToAdd.value,
        price: totalPrice.value,
    };
    try {
        await axios.post("/api/provision/", payload);
        await fetchProvision();
        provisionToAdd.value = {}
    } catch (error) {
        console.log(error.response?.data);
        isError.value = true
        textOfError.value = error.response.data[0]
    }

}

async function fetchProvision() {
    loading.value = true
    const r = await axios.get("/api/provision/")
    provisions.value = r.data;
    loading.value = false
}

async function fetchServices() {
    const s = await axios.get("/api/service/")
    services.value = s.data;
}

async function fetchAccomodattion() {
    const s = await axios.get("/api/accomodattion/")
    accomodattions.value = s.data;
}

async function fetchEmployees() {
    const r = await axios.get("/api/users/?role=1")
    employees.value = r.data;
}

async function fetchClients() {
    const r = await axios.get("/api/users/?role=2")
    clients.value = r.data;
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchProvision()
    await fetchAccomodattion()
    await fetchServices()
    await fetchEmployees()
    await fetchClients()
})

async function onRemoveClick(provision) {
    await axios.delete(`/api/provision/${provision.id}/`);
    await fetchProvision();
}
</script>

<template>

    <div class="mycontainer">

        <h1>Оказание услуг</h1>

        <div class="objects">
            <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#provisionModel">
                Добавить оказание услуги
            </button>
            <div v-if="loading">Данные загружаются, подождите...</div>
            <div v-for="provision in provisions">
                <div class="list">
                    <div> Услуга: {{ findService(provision.service) }}. {{ accomodattionLabel(provision.accomodattion)
                    }}</div>
                    <button class="btn btn-success" @click="onProvisionEditClick(provision)" data-bs-toggle="modal"
                        data-bs-target="#editProvisionModal">
                        <i class="bi bi-pen-fill"> </i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(provision)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>

        <div class="modal fade" id="editProvisionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5">
                            Изменение оказания услуги
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body objects">
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToEdit.service" required>
                                        <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                                    </select>
                                    <label for="floatingInput">Услуга</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="number" class="form-control" :value="totalPrice" readonly />
                                    <label for="floatingInput">Цена</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="number" class="form-control" min="1" max="100"
                                        v-model="provisionToEdit.quantity" required />
                                    <label for="floatingInput">Количество</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToEdit.accomodattion" required>
                                        <option :value="a.id" v-for="a in accomodattions">{{ accomodattionLabel(a.id) }}
                                        </option>
                                    </select>
                                    <label for="floatingInput">Проживание</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToEdit.employee" required>
                                        <option :value="e.id" v-for="e in employees">{{ e.username }}</option>
                                    </select>
                                    <label for="floatingInput">Сотрудник</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-success"
                            @click="onUpdateProvision">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>


        <div class="modal fade" id="provisionModel" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5">
                            Изменение оказания услуги
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body objects">
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToAdd.service" required>
                                        <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                                    </select>
                                    <label for="floatingInput">Услуга</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="number" class="form-control" :value="totalPrice" readonly />
                                    <label for="floatingInput">Цена</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="number" class="form-control" min="1" max="100"
                                        v-model="provisionToAdd.quantity" required />
                                    <label for="floatingInput">Количество</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToAdd.accomodattion" required>
                                        <option :value="a.id" v-for="a in accomodattions">{{ accomodattionLabel(a.id) }}
                                        </option>
                                    </select>
                                    <label for="floatingInput">Проживание</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="provisionToAdd.employee" required>
                                        <option :value="e.id" v-for="e in employees">{{ e.username }}</option>
                                    </select>
                                    <label for="floatingInput">Сотрудник</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-success" @click="onProvisionAdd">
                            Добавить
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <transition name="modal" v-if="isError">
            <div class="modal-mask">
                <div class="modal-wrapper">
                    <div class="modal-container">
                        <div>
                            {{ textOfError }}
                        </div>
                        <div>
                            <button class="modal-default-button" @click="isError = false">
                                OK
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
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


.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}

.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}

.modal-container {
    width: 300px;
    margin: 0px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-family: Helvetica, Arial, sans-serif;
}
</style>
