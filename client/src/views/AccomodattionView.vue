<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, } from 'vue';
import Cookies from 'js-cookie';

const accomodattions = ref([])
let loading = ref(false)
const accomodattionToAdd = ref({});
const accomodattionToEdit = ref({});
let selectedAccomodattion = ref()
const rooms = ref([])
const clients = ref([])
const employees = ref([])

function roomLabel(id) {
    const r = rooms.value.find(x => x.id === id);
    return r ? r.number : id;
}

function clientLabel(id) {
    const c = clients.value.find(x => x.id === id);
    return c.first_name ? c.first_name : c.username;
}

function makePriceComputeds(source) {
    const nights = computed(() => {
        const { in_date, out_date } = source.value || {};
        if (!in_date || !out_date) return 0;
        const diff = Math.round((new Date(out_date) - new Date(in_date)) / 86400000);
        return Number.isFinite(diff) ? diff : 0;
    });

    const totalPrice = computed(() => {
        const roomId = source.value?.room;
        const { in_date, out_date } = source.value || {};
        const room = rooms.value.find(r => r.id === roomId);
        if (!room || nights.value < 0 || !in_date || !out_date) return 0;
        if (nights.value === 0)
            return room.price * 1
        return room.price * nights.value;
    });

    return { nights, totalPrice };
}

const { nights, totalPrice } = makePriceComputeds(accomodattionToAdd);
const { nights: nightsEdit, totalPrice: totalPriceEdit } = makePriceComputeds(accomodattionToEdit);


async function onAccomodattionEditClick(accomodattion) {
    accomodattionToEdit.value = { ...accomodattion };
}

async function onUpdateAccomodattion() {
    const payload = {
        ...accomodattionToEdit.value,
        price: totalPriceEdit.value,
    };
    await axios.put(`/api/accomodattion/${accomodattionToEdit.value.id}/`, payload);
    await fetchAccomodattion();
}

async function onAccomodattionAdd() {
    const payload = {
        ...accomodattionToAdd.value,
        price: totalPrice.value,
    };
    await axios.post("/api/accomodattion/", payload);
    await fetchAccomodattion();
}

async function fetchAccomodattion() {
    loading.value = true
    const r = await axios.get("/api/accomodattion/")
    accomodattions.value = r.data;
    loading.value = false
}

async function fetchRooms() {
    const r = await axios.get("/api/rooms/")
    rooms.value = r.data;
}

async function fetchClients() {
    const r = await axios.get("/api/users/")
    clients.value = r.data;
}

async function fetchEmployees() {
    const r = await axios.get("/api/users/")
    //   ("/api/users/?groups=Сотрудники")
    employees.value = r.data;
}

onBeforeMount(async () => {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    await fetchAccomodattion()
    await fetchRooms()
    await fetchClients()
    await fetchEmployees()
})

async function onRemoveClick(accomodattion) {
    await axios.delete(`/api/accomodattion/${accomodattion.id}/`);
    await fetchAccomodattion();
}
</script>

<template>

    <div class="mycontainer">

        <h1>Проживания</h1>

        <div style="margin-bottom: 10px;">
            <form @submit.prevent.stop="onAccomodattionAdd" class="objects">
                <div class="form-floating">
                    <select class="form-select" v-model="accomodattionToAdd.room" required>
                        <option :value="r.id" v-for="r in rooms">{{ r.number }}</option>
                    </select>
                    <label for="floatingInput">Номер</label>
                </div>
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="accomodattionToAdd.in_date" required />
                    <label for="floatingInput">Дата въезда</label>
                </div>
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="accomodattionToAdd.out_date" required />
                    <label for="floatingInput">Дата выезда</label>
                </div>
                <div class="form-floating">
                    <input type="number" class="form-control" :value="totalPrice" readonly />
                    <label for="floatingInput">Цена</label>
                </div>
                <div class="form-floating">
                    <select class="form-select" v-model="accomodattionToAdd.client" required>
                        <option :value="c.id" v-for="c in clients">{{ c.username }}</option>
                    </select>
                    <label for="floatingInput">Клиенты</label>
                </div>
                <div class="form-floating">
                    <select class="form-select" v-model="accomodattionToAdd.employee" required>
                        <option :value="e.id" v-for="e in employees">{{ e.username }}</option>
                    </select>
                    <label for="floatingInput">Сотрудник</label>
                </div>
                <button class="btn btn-warning" :disabled="nights < 0">
                    Добавить
                </button>
            </form>
        </div>

        <div class="objects">
            <select class="form-select" v-model="selectedAccomodattion">
                <option :value="accomodattion" v-for="accomodattion in accomodattions">
                    Номер {{ roomLabel(accomodattion.room) }}, даты:
                    {{ accomodattion.in_date }}:{{ accomodattion.out_date }},
                    клиент: {{ clientLabel(accomodattion.client) }}
                </option>
            </select>
            <button class="btn btn-success" @click="onAccomodattionEditClick(selectedAccomodattion)"
                data-bs-toggle="modal" data-bs-target="#editAccomodattionModal">
                <i class="bi bi-pen-fill"> Редактировать</i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(selectedAccomodattion)">
                <i class="bi bi-x"> Удалить проживание</i>
            </button>
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
                                    <input type="number" class="form-control" :value="totalPriceEdit" readonly />
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
                                    <label for="floatingInput">Клиенты</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToEdit.employee" required>
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
                        <button data-bs-dismiss="modal" type="button" class="btn btn-success" :disabled="nightsEdit < 0"
                            @click="onUpdateAccomodattion">
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
