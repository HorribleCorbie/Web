<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, watch } from 'vue';
import Cookies from 'js-cookie';
import SearchFilters from '@/components/SearchFilters.vue'
import ErrorModal from '@/components/ErrorModal.vue';
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';
import CreateProvision from '@/components/CreateProvision.vue';
import CreateStatistics from '@/components/CreateStatistics.vue';
import SearchProvision from '@/components/SearchProvision.vue';
import SearchAccommodattion from '@/components/SearchAccommodattion.vue';

const profileStore = useProfileStore();
const {
    isSuperUser,
    id,
    thisCanBeAddAndChanged
} = storeToRefs(profileStore)

let provisionModal = ref(false)

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


const isFormStats = ref(false)

const totalPrice = computed(() => {
    if (provisionToEdit.value.quantity != undefined && provisionToEdit.value.service) {
        const quantity = provisionToEdit.value.quantity
        const service = services.value.find(x => x.id === provisionToEdit.value.service)
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


function findAccomodattion(id_accomodattion) {
    const accomodattion = accomodattions.value.find(x => x.id === id_accomodattion)
    return accomodattion
}

function findService(id_service) {
    const s = services.value.find(x => x.id === id_service)
    return s ? s.name : id_service
}

async function onProvisionEditClick(provision) {
    console.log('Исходный объект:', provision);
    provisionToEdit.value = { ...provision };
    console.log('Объект для редактирования:', provisionToEdit.value);
}

async function onUpdateProvision() {
    const payload = {
        quantity: provisionToEdit.value.quantity,
        service: provisionToEdit.value.service,
        accomodattion: provisionToEdit.value.accomodattion,
        employee: provisionToEdit.value.employee,
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


async function fetchServices() {
    const s = await axios.get("/api/service/", { params: { all: 1 } })
    services.value = s.data;
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


const page = ref(1)
const pageItemsCount = ref(10)
const authorFilter = ref(null)
const serviceFilter = ref(null)
const quantityFilter = ref(null)
const priceFilter = ref(null)

const clientFilter = ref(null)
const numberFilter = ref(null)
const inDateFilter = ref(null)
const outDateFilter = ref(null)

async function fetchProvision() {
    loading.value = true
    const params = { page: page.value, page_size: pageItemsCount.value }
    if (authorFilter.value) params.user = authorFilter.value
    if (serviceFilter.value) params.service = serviceFilter.value
    if (quantityFilter.value) params.quantity = quantityFilter.value
    if (priceFilter.value) params.price = priceFilter.value

    if (clientFilter.value) params.client = clientFilter.value
    if (numberFilter.value) params.number = numberFilter.value
    if (inDateFilter.value) params.in_date = inDateFilter.value
    if (outDateFilter.value) params.out_date = outDateFilter.value
    const r = await axios.get('/api/provision/', { params })
    provisions.value = r.data.results
    pagesCount.value = Math.max(1, Math.ceil(r.data.count / pageItemsCount.value))
    loading.value = false
}

watch([authorFilter, serviceFilter, quantityFilter,
    priceFilter, clientFilter, numberFilter, inDateFilter, outDateFilter], () => {
        if (page.value === 1) fetchProvision()
        else page.value = 1
    })

const pagesCount = ref()

watch(page, () => {
    fetchProvision();
})

function label(name) {
    return name.user_first_name ? name.user_first_name : name.user_name
}

function exportExel() {
  axios({
    url: '/api/provision/export',
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
            <h1>Оказание услуг</h1>
            <button class="btn btn-info" v-if="isSuperUser" @click="isFormStats = true"
                style="position:absolute; top: 0; right: 0;">
                <i class="bi bi-graph-up"></i>
            </button>
            <button class="btn btn-info" v-if="isSuperUser" @click="exportExel()"
                style="position:absolute; top: 0; left: 0;">
                <i class="bi bi-arrow-down-square"></i>
            </button>
        </div>

        <div class="objects">
            <button type="button" class="btn btn-warning" @click="provisionModal = true">
                Добавить оказание услуги
            </button>
            <div v-if="loading">Данные загружаются, подождите...</div>
            <search-filters v-if="isSuperUser" v-model="authorFilter" :type="'provision'" />
            <SearchProvision v-model:name="serviceFilter" v-model:quantity="quantityFilter"
                v-model:price="priceFilter" />
            <div style="text-align: center;">Поиск по проживанию</div>
            <SearchAccommodattion v-model:client="clientFilter" v-model:in_date="inDateFilter"
                v-model:number="numberFilter" v-model:out_date="outDateFilter" :needPrice="false" />
            <div v-if="!loading && provisions.length == 0" style="text-align: center;">У вас нет оказанных услуг</div>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Услуга</th>
                        <th scope="col">Проживание</th>
                        <th scope="col">Количество</th>
                        <th scope="col">Цена</th>
                        <th v-if="thisCanBeAddAndChanged" scope="col">Управление</th>
                        <th v-if="isSuperUser" scope="col">Автор</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="provision in provisions">
                        <td>{{ findService(provision.service) }}</td>
                        <td>Клиент - {{ provision.accomodattion_info.client_name }} в номере {{
                            provision.accomodattion_info.room_number }} с даты
                            {{ provision.accomodattion_info.in_date }} по {{ provision.accomodattion_info.out_date }}
                        </td>
                        <td>{{ provision.quantity }}</td>
                        <td>{{ provision.price }}</td>
                        <td v-if="(provision.user === id || isSuperUser) && thisCanBeAddAndChanged">
                            <div class="buttons-div">
                                <button class="btn btn-success" @click="onProvisionEditClick(provision)"
                                    data-bs-toggle="modal" data-bs-target="#editProvisionModal">
                                    <i class="bi bi-pen-fill"></i>
                                </button>
                                <button class="btn btn-danger" @click="selectedProvision = provision"
                                    data-bs-toggle="modal" data-bs-target="#deleteModal">
                                    <i class="bi bi-x"></i>
                                </button>
                            </div>
                        </td>
                        <td v-if="isSuperUser">{{ label(provision) }}</td>
                    </tr>
                </tbody>
            </table>

            <nav aria-label="Page navigation example">
                <ul class="pagination justify-content-center">
                    <li class="page-item " v-if="page > 1" @click="page -= 1">
                        <a class="page-link" href="#">Previous</a>
                    </li>

                    <li @click="page = page - 1" class="page-item" v-if="page - 1 > 0"><a class="page-link">{{ page - 1
                    }}</a>
                    </li>
                    <li class="page-item" v-if="page > 0"><span href="" class="page-link">{{ page }}</span></li>
                    <li @click="page = page + 1" class="page-item" v-if="page + 1 < pagesCount"><a class="page-link">{{
                        page + 1
                            }}</a></li>
                    <li @click="page = page + 2" class="page-item" v-if="page + 2 < pagesCount"><a class="page-link">{{
                        page + 2
                            }}</a></li>
                    <li @click="page = page + 3" class="page-item" v-if="page + 3 < pagesCount"><a class="page-link">{{
                        page + 3
                            }}</a></li>

                    <li class="page-item" v-if="page < pagesCount">
                        <a class="page-link" href="#" @click="page += 1">Next</a>
                    </li>
                </ul>
            </nav>

        </div>

        <CreateStatistics v-model="isFormStats" :type="'provision'" />


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
                                    <select class="form-select" disabled v-model="provisionToEdit.accomodattion"
                                        required>
                                        <option :value="provisionToEdit.accomodattion"> Клиент - {{
                                            provisionToEdit.accomodattion_info?.client_name }}
                                            в номере {{ provisionToEdit.accomodattion_info?.room_number }}
                                            с даты {{ provisionToEdit.accomodattion_info?.in_date }}
                                            по {{ provisionToEdit.accomodattion_info?.out_date }}
                                        </option>
                                    </select>
                                    <label for="floatingInput">Проживание</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
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
            :clients="clients" :employees="thisCanBeAddAndChanged ? employees : undefined" @success="fetchProvision" />

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
