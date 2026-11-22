<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import axios from 'axios';
import useProfileStore from '../stores/profileStore';
import { Modal } from 'bootstrap';
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const {
    id,
} = storeToRefs(profileStore)

const props = defineProps({
    rooms: {
        type: Array,
        required: true
    },
    clients: {
        type: Array,
        required: true
    },
})
const client = ref(props.clients[0].id)

const accomodattionToAdd = ref({})
const accomodattionModal = defineModel({ type: Boolean, default: false })

const emit = defineEmits(['success']);

const isFormValid = computed(() => {
    if (!accomodattionToAdd.value || Object.keys(accomodattionToAdd.value).length === 0) {
        return false;
    }
    const { room, in_date, out_date } = accomodattionToAdd.value;
    return (room && in_date && out_date);
});

const modalRef = ref([])
let bootstrapInstance = null

onMounted(() => {
    bootstrapInstance = Modal.getOrCreateInstance(modalRef.value);

    modalRef.value.addEventListener('hidden.bs.modal', onModalHidden);

    if (accomodattionModal.value) {
        bootstrapInstance.show();
    }
});

watch(accomodattionModal, (isOpen) => {
    if (!bootstrapInstance) return;

    if (isOpen) {
        bootstrapInstance.show();
    } else {
        bootstrapInstance.hide();
    }
});

function onModalHidden() {
    clearForm();
    accomodattionModal.value = false;
}

function closeModal() {
    bootstrapInstance?.hide();
}

onBeforeUnmount(() => {
    modalRef.value?.removeEventListener('hidden.bs.modal', onModalHidden);
    bootstrapInstance?.dispose();
});

function clearForm() {
    accomodattionToAdd.value = {
        room: null,
        in_date: '',
        out_date: ''
    };
}

const totalPrice = computed(() => {
    const { in_date, out_date , room} = accomodattionToAdd.value || {}

    if (!in_date || !out_date || !room) return 0

    const roomNumber = props.rooms.find(r => r.id === room)

    const diff = Math.round((new Date(out_date) - new Date(in_date)) / 86400000);
    const result = diff + 1;
    const days = Number.isFinite(result) && result > 0 ? result : 0

    if (!roomNumber || days <= 0) return 0

    return roomNumber.price * days
})

async function onAccomodattionAdd() {
    const payload = {
        ...accomodattionToAdd.value,
        price: totalPrice.value,
        client: client.value,
        user: id.value
    }
    await axios.post("/api/accomodattion/", payload);
    closeModal();
    emit('success')
}

</script>

<template>
    <div class="modal fade" id="accomodattionModal" ref="modalRef" tabindex="-1">
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
                                <input type="date" class="form-control" v-model="accomodattionToAdd.in_date" required />
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
                    <div class="row" v-if="clients.length >= 2">
                        <div class="col">
                            <div class="form-floating">
                                <select class="form-select" v-model="client" required>
                                    <option selected :value="c.id" v-for="c in clients">{{ c.username }}</option>
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
                    <button type="button" :disabled="!isFormValid" class="btn btn-success" @click="onAccomodattionAdd">
                        Добавить
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>