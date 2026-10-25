<script setup>
const props = defineProps({
    textOfError: {
        type: String,
        default: 'error'
    }
})
const isError = defineModel({ type: Boolean, default: false })
</script>
<template>
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
</template>