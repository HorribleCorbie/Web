<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, } from 'vue';
import Cookies from 'js-cookie';

const provisions = ref([])
let loading = ref(false)
const provisionToAdd = ref({});
const provisionToEdit = ref({});
let selectedProvision = ref()
const accomodattions = ref([])
const clients = ref([])
const employees = ref([])
const services = ref([])

function makePriceComputeds(source) {
    const totalPrice = computed(() => {
        if (source.value.quantity != undefined && source.value.service) {
            const quantity = source.value.quantity
            const service = services.value.find(x => x.id === source.value.service)
            return quantity * service.price
        }
        return 0
    });

    return { totalPrice };
}

const { totalPrice } = makePriceComputeds(provisionToAdd)
const { totalPrice: totalPriceEdit } = makePriceComputeds(provisionToEdit)

function findCLient(id_accomodattion) {
    const accomodattion = findAccomodattion(id_accomodattion)
    if (accomodattion != undefined) {
        const client = clients.value.find(x => x.id === accomodattion.client)
        return client!= undefined ? (client.first_name ? client.first_name : client.username) : id_accomodattion
    }
}

function accomodattionLabel(id) {
    const acc = findAccomodattion(id);
    if (acc!= undefined) return `Клиент: ${findCLient(id)}, даты: ${acc.in_date}:${acc.out_date}`;
}

function findAccomodattion(id_accomodattion) {
    const accomodattion = accomodattions.value.find(x => x.id === id_accomodattion)
    return accomodattion
}

function findService(id_service) {
    const s = services.value.find(x => x.id === id_service)
    return s ? s.name : id_service
}

async function fetchClients() {
    const r = await axios.get("/api/users/")
    clients.value = r.data;
}

async function onProvisionEditClick(provision) {
    provisionToEdit.value = { ...provision };
}

async function onUpdateProvision() {
    const payload = {
        ...provisionToEdit.value,
        price: totalPriceEdit.value,
    };
    await axios.put(`/api/provision/${provisionToEdit.value.id}/`, payload);
    await fetchProvision();
}

async function onProvisionAdd() {
    const payload = {
        ...provisionToAdd.value,
        price: totalPrice.value,
    };
    await axios.post("/api/provision/", payload);
    await fetchProvision();
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
    const r = await axios.get("/api/users/")
    //   ("/api/users/?groups=Сотрудники")
    employees.value = r.data;
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

        <div style="margin-bottom: 10px;">
            <form @submit.prevent.stop="onProvisionAdd" class="objects">
                <div class="form-floating">
                    <select class="form-select" v-model="provisionToAdd.service" required>
                        <option :value="s.id" v-for="s in services">{{ s.name }}</option>
                    </select>
                    <label for="floatingInput">Услуга</label>
                </div>
                <div class="form-floating">
                    <input type="number" class="form-control" min="1" max="100" v-model="provisionToAdd.quantity"
                        required />
                    <label for="floatingInput">Количество</label>
                </div>
                <div class="form-floating">
                    <input type="number" class="form-control" :value="totalPrice" readonly />
                    <label for="floatingInput">Сумма</label>
                </div>
                <div class="form-floating">
                    <select class="form-select" v-model="provisionToAdd.accomodattion" required>
                        <option :value="a.id" v-for="a in accomodattions">
                            {{accomodattionLabel(a.id)}} </option>
                    </select>
                    <label for="floatingInput">Проживание</label>
                </div>
                <div class="form-floating">
                    <select class="form-select" v-model="provisionToAdd.employee" required>
                        <option :value="e.id" v-for="e in employees">{{ e.username }}</option>
                    </select>
                    <label for="floatingInput">Сотрудник</label>
                </div>
                <button class="btn btn-warning">
                    Добавить
                </button>
            </form>
        </div>

        <div class="objects">
            <select class="form-select" v-model="selectedProvision">
                <option :value="provision" v-for="provision in provisions">
                    Услуга {{ findService(provision.service) }}, {{accomodattionLabel(provision.accomodattion)}}
                </option>
            </select>
            <button class="btn btn-success" @click="onProvisionEditClick(selectedProvision)" data-bs-toggle="modal"
                data-bs-target="#editProvisionModal">
                <i class="bi bi-pen-fill"> Редактировать</i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(selectedProvision)">
                <i class="bi bi-x"> Удалить оказание услуги</i>
            </button>
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
                                    <input type="number" class="form-control" :value="totalPriceEdit" readonly />
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
                                        <option :value="a.id" v-for="a in accomodattions">{{accomodattionLabel(a.id)}}
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
