<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import axios from 'axios';
import useProfileStore from '../stores/profileStore';
import ErrorModal from '@/components/ErrorModal.vue';
import { Modal } from 'bootstrap';
import { storeToRefs } from 'pinia';


const props = defineProps({
    services: {
        type: Array,
        required: true
    },
    accomodattions: {
        type: Array,
        required: true
    },
    clients: {
        type: Array,
        required: true
    },
    employees: {
        type: Array,
        required: false,
    },
})

const provisionToAdd = ref({})
const provisionModal = defineModel({ type: Boolean, default: false })

const emit = defineEmits(['success'])

const isFormValid = computed(() => {
    if (!provisionToAdd.value || Object.keys(provisionToAdd.value).length === 0) {
        return false
    }
    const { service, quantity, accomodattion } = provisionToAdd.value
    return (service && totalPrice.value > 0 && Number(quantity) > 0 && accomodattion)
})

const profileStore = useProfileStore();
const {
    id,
} = storeToRefs(profileStore)

const modalRef = ref([])
let bootstrapInstance = null

onMounted(() => {
    bootstrapInstance = Modal.getOrCreateInstance(modalRef.value);

    modalRef.value.addEventListener('hidden.bs.modal', onModalHidden);

    if (provisionModal.value) {
        bootstrapInstance.show();
    }
});

watch(provisionModal, (isOpen) => {
    if (!bootstrapInstance) return;

    if (isOpen) {
        bootstrapInstance.show();
    } else {
        bootstrapInstance.hide();
    }
});

function onModalHidden() {
    clearForm();
    provisionModal.value = false;
}

function closeModal() {
    bootstrapInstance?.hide();
}

onBeforeUnmount(() => {
    modalRef.value?.removeEventListener('hidden.bs.modal', onModalHidden);
    bootstrapInstance?.dispose();
});

function clearForm() {
    provisionToAdd.value = {
        service: null,
        accomodattion: null,
        price: null,
        quantity: null,
        employee: null
    };
}

let isError = ref(false)
let textOfError = ref()


const totalPrice = computed(() => {
    if (provisionToAdd.value.quantity != undefined && provisionToAdd.value.service) {
        const quantity = provisionToAdd.value.quantity
        const service = props.services.find(x => x.id === provisionToAdd.value.service)
        return quantity * service.price
    }
    return 0
});


function accomodattionLabel(id) {
    const acc = findAccomodattion(id);
    if (acc != undefined) return `Клиент: ${acc.client_name ? acc.client_name : acc.client_user}, даты: ${acc.in_date} по ${acc.out_date}`;
}

function findAccomodattion(id_accomodattion) {
    const accomodattion = props.accomodattions.find(x => x.id === id_accomodattion)
    return accomodattion
}

async function onProvisionAdd() {
    const payload = {
        ...provisionToAdd.value,
        price: totalPrice.value,
        user: id.value
    };
    try {
        await axios.post("/api/provision/", payload);
        closeModal()
        emit('success')
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
            textOfError.value = responseData
        } else {
            textOfError.value = error.message || 'Неизвестная ошибка';
        }

    }

}

</script>
<template>
    <div class="modal fade" id="provisionModel" ref="modalRef" tabindex="-1">
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
                    <div class="row" v-if="accomodattions.length == 0">
                        <div class="col">
                            У вас нет активных проживаний, создать оказание услуг невозможно
                        </div>
                    </div>
                    <div class="row" v-if="accomodattions.length == 0">
                        <div class="col">
                           {{ provisionToAdd.accomodattion }}
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
                        <div class="col" v-if="employees">
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
                    <button :disabled="!isFormValid" type="button" class="btn btn-success" @click="onProvisionAdd">
                        Добавить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <ErrorModal v-if="isError" v-model="isError" :textOfError="textOfError" />
</template>