<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, } from 'vue';
import Cookies from 'js-cookie';
import SearchFilters from '@/components/SearchFilters.vue'
import ErrorModal from '@/components/ErrorModal.vue';
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';
import CreateProvision from '@/components/CreateProvision.vue';

const filteredProvisions = ref([])

const profileStore = useProfileStore();
const {
    isSuperUser,
    id,
    thisCanBeAddAndChanged
} = storeToRefs(profileStore)

let provisionModal = ref(false)

const provisionToAdd = ref({});
const provisionToEdit = ref({});
const selectedProvision = ref({})

const provisions = ref([])
const accomodattions = ref([])
const activeAccomodattions = ref([])
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
        user: id.value
    };
    try {
        await axios.put(`/api/provision/${provisionToEdit.value.id}/`, payload);
        await fetchProvision();
        provisionToEdit.value = {}
    } catch (error) {
        isError.value = true;
        const responseData = error.response?.data
        if (Array.isArray(responseData)) {
            textOfError.value = responseData.join('\n')
        } else if (typeof responseData === 'object') {
            const errorMessages = [];

            for (const [field, messages] of Object.entries(responseData)) {

                const fieldMessages = Array.isArray(messages) ? messages.join(', ') : messages;

                errorMessages.push(`${field}: ${fieldMessages}`);
            }

            textOfError.value = errorMessages.join('\n');
        } else if (typeof responseData === 'string') {
            textOfError.value = allErrors
        } else {
            textOfError.value = error.message || 'Неизвестная ошибка';
        }
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

    const today = new Date().toISOString().split('T')[0];

    activeAccomodattions.value = accomodattions.value.filter(x => x.in_date <= today && x.out_date >= today)
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
            <button type="button" class="btn btn-warning" @click="provisionModal=true">
                Добавить оказание услуги
            </button>
            <div v-if="loading">Данные загружаются, подождите...</div>
            <div v-if="!loading && provisions.length == 0">У вас нет оказанных услуг</div>
            <div v-if="provisions != null && isSuperUser">
                <search-filters :items="provisions"
                    @update:filtered-items="filteredProvisions = $event"></search-filters>
            </div>
            <div v-for="provision in (isSuperUser ? filteredProvisions : provisions)">
                <div class="list">
                    <div> Услуга: {{ findService(provision.service) }}. {{ accomodattionLabel(provision.accomodattion)
                        }}</div>
                    <div class="buttons-div" v-if="(provision.user === id || isSuperUser) && thisCanBeAddAndChanged">
                        <button class="btn btn-success" @click="onProvisionEditClick(provision)" data-bs-toggle="modal"
                            data-bs-target="#editProvisionModal">
                            <i class="bi bi-pen-fill"> </i>
                        </button>
                        <button class="btn btn-danger" @click="selectedProvision = provision" data-bs-toggle="modal"
                            data-bs-target="#deleteModal">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>

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

        <CreateProvision v-model="provisionModal" :services="services" :accomodattions="activeAccomodattions"
            :clients="clients" :employees="thisCanBeAddAndChanged?employees:undefined" @success="fetchProvision" />

        <ErrorModal v-if="isError" v-model="isError" :textOfError="textOfError" />

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
                                Вы точно хотите удалить оказания услуги {{ findService(selectedProvision.service) }} для
                                {{
                                    findCLient(selectedProvision.accomodattion) }}?
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-danger"
                            @click="onRemoveClick(selectedProvision)">
                            Удалить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped></style>
