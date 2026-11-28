import { defineStore } from "pinia";
import { ref } from 'vue';

const useErrorStore = defineStore('errorStore', () =>{

    const textOfError = ref('')
    const isError = ref(false)

    function showError(text){
        textOfError.value = text
        isError.value = true
    }

    return {
        textOfError,
        isError,
        showError
    }
})

export default useErrorStore