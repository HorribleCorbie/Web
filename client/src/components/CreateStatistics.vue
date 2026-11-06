<script setup>
import { onBeforeUnmount, ref, onMounted, watch } from 'vue'
import { Modal } from 'bootstrap';
import axios from 'axios'

const props = defineProps({
    type: {
        type: String,
        required: true
    }
})

const stats = ref({})

const isFormStats = defineModel({ type: Boolean, default: false })

const modalRef = ref(null)
let bootstrapInstance = null

const fetchStats = async () => {
  try {
    const r = await axios.get(`/api/${props.type}/stats/`);
    stats.value = r.data;
  } catch (error) {
    console.error("Ошибка при загрузке статистики:", error);
  }
}

onMounted(() => {
    bootstrapInstance = Modal.getOrCreateInstance(modalRef.value);

    modalRef.value.addEventListener('hidden.bs.modal', onModalHidden);

    if (isFormStats.value) {
        bootstrapInstance.show();
        fetchStats()
    }
});

function onModalHidden() {
    isFormStats.value = false;
}

watch(isFormStats, (newVal) => {
  if (newVal) {
    bootstrapInstance?.show();
    fetchStats();
  } else {
    bootstrapInstance?.hide();
  }
})

onBeforeUnmount(() => {
  if (modalRef.value) {
    modalRef.value.removeEventListener('hidden.bs.modal', onModalHidden);
  }
  bootstrapInstance?.dispose();
  isFormStats.value = false
});
</script>


<template>
    <div class="modal fade" id="statsModal" ref="modalRef" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        Статистика
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body objects">
                    <div class="row">
                        <div class="col">
                            Общее количество записей: {{ stats.count }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Средняя цена: {{ stats.avg?.toFixed(2)}}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Максимум: {{ stats.max }}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            Минимум: {{ stats.min }}
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="isFormStats = false">
                        Закрыть
                    </button>
                </div>
            </div>
        </div>
    </div>

</template>