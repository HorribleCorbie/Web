import { createApp } from 'vue'
import { createPinia, storeToRefs } from 'pinia'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.min.css"
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import "bootstrap/dist/js/bootstrap"
import './assets/style.css'
import useErrorStore from './stores/errorStore'

import App from './App.vue'
import router from './router'
import { isArray } from 'lodash'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

const errorStore = useErrorStore()

const textOfError = (error) => {
    if (!error?.response){
        return "Проверьте соединение с интернетом, сервер не отвечает."
    }
        
    const status = error.response.status

    if (status >= 500) {
        return "Проблема на стороне сервера, мы уже работаем над ее устранением."
    }

    const statusMessages = {
        400: 'Некорректные данные в запросе. Проверьте правильность заполнения полей.',
        401: 'Необходимо войти в систему.',
        403: 'Отказано в доступе. У вас нет прав для выполнения этого действия.',
        404: 'Запрашиваемый ресурс или страница не найдены.',
        405: 'Метод запроса не поддерживается.',
        429: 'Слишком много запросов. Пожалуйста, подождите немного.'
    }
    
    const data = error.response.data
    const text = isArray(data)? data.join(','): typeof data === 'string' || data.detail || data.message || data.error

    const answer = text || statusMessages[status]

    if (answer == "You do not have permission to perform this action.")
        return statusMessages[403]
    if ( answer == "Authentication credentials were not provided")
        return statusMessages[401]

    return answer
}

app.config.errorHandler = (err, vm, info) => {
    errorStore.showError(textOfError(err))
}

window.addEventListener('unhandledrejection', event => {
    errorStore.showError(textOfError(event.reason))
});