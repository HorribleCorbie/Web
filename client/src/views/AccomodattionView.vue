<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref, } from 'vue';
import Cookies from 'js-cookie';

const accomodattionToAdd = ref({});
const accomodattionToEdit = ref({});

const accomodattions = ref([])
const rooms = ref([])
const clients = ref([])
const employees = ref([])

let loading = ref(false)
let isError = ref(false)
let textOfError = ref()

function roomLabel(id) {
    const r = rooms.value.find(x => x.id === id);
    return r ? r.number : id;
}

function clientLabel(id) {
    const c = clients.value.find(x => x.id === id);
    return c != undefined ? (c.first_name ? c.first_name : c.username) : id
}

const source = computed(() => {
    return accomodattionToEdit.value.id
        ? accomodattionToEdit.value
        : accomodattionToAdd.value
})

const nights = computed(() => {
    const { in_date, out_date } = source.value || {};
    if (!in_date || !out_date) return 0;
    const diff = Math.round((new Date(out_date) - new Date(in_date)) / 86400000);
    nights.value = nights.value + 1
    return Number.isFinite(diff) ? diff + 1 : 0;
});

const totalPrice = computed(() => {
    const roomId = source.value?.room;
    const { in_date, out_date } = source.value || {};
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
    }catch(error){
        isError.value = true;
        textOfError.value = error.response.data[0];
    }
    
}

async function onAccomodattionAdd() {
    const payload = {
        ...accomodattionToAdd.value,
        price: totalPrice.value,
    };
    try {
        await axios.post("/api/accomodattion/", payload);
        accomodattionToAdd.value = {};
        await fetchAccomodattion();
    } catch (error) {
        isError.value = true;
        textOfError.value = error.response.data[0];
    }
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
        <div class="objects">
            <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#accomodattionModal">
                Добавить проживание
            </button>
            <div v-if="loading">Данные загружаются, подождите...</div>
            <div v-for="accomodattion in accomodattions">
                <div class="list">
                    <div> Номер {{ roomLabel(accomodattion.room) }}, даты:
                        {{ accomodattion.in_date }}:{{ accomodattion.out_date }},
                        клиент: {{ clientLabel(accomodattion.client) }}
                    </div>
                    <button class="btn btn-success" @click="onAccomodattionEditClick(accomodattion)"
                        data-bs-toggle="modal" data-bs-target="#editAccomodattionModal">
                        <i class="bi bi-pen-fill"> </i>
                    </button>
                    <button class="btn btn-danger" @click="onRemoveClick(accomodattion)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
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
                        <button data-bs-dismiss="modal" type="button" class="btn btn-success"
                            @click="onUpdateAccomodattion">
                            Сохранить
                        </button>
                    </div>
                </div>
            </div>
        </div>


        <div class="modal fade" id="accomodattionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5">
                            Добавить проживание
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body objects">
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToAdd.room" required>
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
                                    <input type="date" class="form-control" v-model="accomodattionToAdd.in_date"
                                        required />
                                    <label for="floatingInput">Дата въезда</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <input type="date" class="form-control" v-model="accomodattionToAdd.out_date"
                                        required />
                                    <label for="floatingInput">Дата выезда</label>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToAdd.client" required>
                                        <option :value="c.id" v-for="c in clients">{{ c.username }}</option>
                                    </select>
                                    <label for="floatingInput">Клиенты</label>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-floating">
                                    <select class="form-select" v-model="accomodattionToAdd.employee" required>
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
                            @click="onAccomodattionAdd">
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
