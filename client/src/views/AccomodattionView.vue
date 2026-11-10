<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, watch } from 'vue';
import Cookies from 'js-cookie';
import SearchFilters from '@/components/SearchFilters.vue'
import CreateAccommodattion from '@/components/CreateAccommodattion.vue';
import ErrorModal from '@/components/ErrorModal.vue';
import { storeToRefs } from 'pinia';
import useProfileStore from '../stores/profileStore';
import CreateStatistics from '@/components/CreateStatistics.vue';
import SearchAccommodattion from '@/components/SearchAccommodattion.vue';

const accomodattionToEdit = ref({})
const selectedAccomodattion = ref([])

const accomodattions = ref([])
const rooms = ref([])
const clients = ref([])

let loading = ref(false)
let isError = ref(false)
let textOfError = ref('')
let accomodattionModal = ref(false)

const profileStore = useProfileStore();
const {
    isSuperUser,
    id,
    thisCanBeAddAndChanged,
    userName
} = storeToRefs(profileStore)

const isFormStats = ref(false)

const nights = computed(() => {
    const { in_date, out_date } = accomodattionToEdit.value || {};
    if (!in_date || !out_date) return 0;
    const diff = Math.round((new Date(out_date) - new Date(in_date)) / 86400000);
    const result = diff + 1;
    return Number.isFinite(result) && result > 0 ? result : 0;
});

const totalPrice = computed(() => {
    const roomId = accomodattionToEdit.value?.room;
    const { in_date, out_date } = accomodattionToEdit.value || {};
    const room = rooms.value.find(r => r.id === roomId);
    if (!room || nights.value <= 0 || !in_date || !out_date) return 0;
    return room.price * nights.value;
});



async function onAccomodattionEditClick(accomodattion) {
    accomodattionToEdit.value = { ...accomodattion };
}

async function onUpdateAccomodattion() {
    const payload = {
        ...accomodattionToEdit.value,
        price: totalPrice.value,
    };
    try {
        await axios.put(`/api/accomodattion/${accomodattionToEdit.value.id}/`, payload);
        accomodattionToEdit.value = {};
        await fetchAccomodattion();
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

async function fetchClients() {
    const r = await axios.get("/api/users/?role=2", { params: { all: 1 } })
    clients.value = r.data;
}


async function fetchRooms() {
    const r = await axios.get("/api/rooms/", { params: { all: 1 } })
    rooms.value = r.data;
}


onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchAccomodattion()
    await fetchRooms()
    await fetchClients()
})

async function onRemoveClick(accomodattion) {
    await axios.delete(`/api/accomodattion/${accomodattion.id}/`);
    await fetchAccomodattion();
}


const page = ref(1)
const pageItemsCount = ref(10)
const authorFilter = ref(null)
const numberFilter = ref(null)
const inDateFilter = ref(null)
const outDateFilter = ref(null)
const clientFilter = ref(null)
const priceFilter = ref(null)

async function fetchAccomodattion() {
    loading.value = true
    const params = { page: page.value, page_size: pageItemsCount.value }
    if (authorFilter.value) params.user = authorFilter.value
    if (numberFilter.value) params.number = numberFilter.value
    if (inDateFilter.value) params.in_date = inDateFilter.value
    if (outDateFilter.value) params.out_date = outDateFilter.value
    if (clientFilter.value) params.client = clientFilter.value
    if (priceFilter.value) params.price = priceFilter.value
    const r = await axios.get('/api/accomodattion/', { params })
    accomodattions.value = r.data.results
    pagesCount.value = Math.max(1, Math.ceil(r.data.count / pageItemsCount.value))
    loading.value = false
}

watch([authorFilter, numberFilter, inDateFilter, outDateFilter, clientFilter, priceFilter], () => {
    if (page.value === 1) fetchAccomodattion()
    else page.value = 1
})

const pagesCount = ref()

watch(page, () => {
    fetchAccomodattion();
})

function label(name) {
    return name.user_first_name ? name.user_first_name : name.user_name
}

function client_label(name) {
    return name.client_name ? name.client_name : name.client_user
}
function exportExel() {
    axios({
        url: '/api/accomodattion/export',
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
            <h1>Проживания</h1>
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
            <button type="button" class="btn btn-warning" @click="accomodattionModal = true">
                Добавить проживание
            </button>
            <div v-if="loading">Данные загружаются, подождите...</div>
            <search-filters v-if="isSuperUser" v-model="authorFilter" :type="'accomodattion'" />
            <SearchAccommodattion v-model:client="clientFilter" v-model:in_date="inDateFilter"
                v-model:number="numberFilter" v-model:out_date="outDateFilter" v-model:price="priceFilter" />

            <div v-if="!loading && accomodattions.length == 0" style="text-align: center;">У вас нет проживаний</div>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Номер комнаты</th>
                        <th scope="col">Дата заселения</th>
                        <th scope="col">Дата выезда</th>
                        <th scope="col">Сумма</th>
                        <th scope="col">Клиент</th>
                        <th v-if="thisCanBeAddAndChanged" scope="col">Управление</th>
                        <th v-if="isSuperUser" scope="col">Автор</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="accomodattion in accomodattions">
                        <td>{{ accomodattion.room_number }}</td>
                        <td>{{ accomodattion.in_date }}</td>
                        <td>{{ accomodattion.out_date }}</td>
                        <td>{{ accomodattion.price }}</td>
                        <td>{{ client_label(accomodattion) }}</td>
                        <td v-if="(accomodattion.user === id || isSuperUser) && thisCanBeAddAndChanged">
                            <div class="buttons-div">
                                <button class="btn btn-success" @click="onAccomodattionEditClick(accomodattion)"
                                    data-bs-toggle="modal" data-bs-target="#editAccomodattionModal">
                                    <i class="bi bi-pen-fill"></i>
                                </button>
                                <button class="btn btn-danger" @click="selectedAccomodattion = accomodattion"
                                    data-bs-toggle="modal" data-bs-target="#deleteModal">
                                    <i class="bi bi-x"></i>
                                </button>
                            </div>
                        </td>
                        <td v-if="isSuperUser">{{ label(accomodattion) }}</td>
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


        <div class="modal fade" id="editAccomodattionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5">
                            Изменение проживание
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body objects">
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToEdit.room" required>
                                        <option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
                                    </select>
                                    <label for="floatingInput">Номер</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="number" class="form-control" :value="totalPrice" readonly />
                                    <label for="floatingInput">Цена</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <input type="date" class="form-control" v-model="accomodattionToEdit.in_date"
                                        required />
                                    <label for="floatingInput">Дата въезда</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="date" class="form-control" v-model="accomodattionToEdit.out_date"
                                        required />
                                    <label for="floatingInput">Дата выезда</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToEdit.client" required>
                                        <option :value="c.id" v-for="c in clients">{{ c.username }}</option>
                                    </select>
                                    <label for="floatingInput">Клиент</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-success"
                            @click="onUpdateAccomodattion">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>


        <CreateAccommodattion v-if="accomodattionModal" v-model="accomodattionModal"
            :clients="(thisCanBeAddAndChanged) ? clients : [{ id: id, username: userName }]" :rooms="rooms"
            @success="fetchAccomodattion" />

        <CreateStatistics v-model="isFormStats" :type="'accomodattion'" />

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
                                Вы точно хотите удалить проживание с {{ selectedAccomodattion.in_date }} по {{
                                    selectedAccomodattion.out_date }} в {{ selectedAccomodattion.room }}?
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal">
                            Закрыть
                        </button>
                        <button data-bs-dismiss="modal" type="button" class="btn btn-danger"
                            @click="onRemoveClick(selectedAccomodattion)">
                            Удалить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped></style>
