import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.min.css"
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import "bootstrap/dist/js/bootstrap"
import './assets/style.css'
import Notifications from '@kyvg/vue3-notification'
import {useNotification} from '@kyvg/vue3-notification'

import App from './App.vue'
import router from './router'
import { isArray } from 'lodash'
const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Notifications)

app.mount('#app')

const { notify }  = useNotification()

const textOfError = (error) => {
    if (!error?.response) {
        return "Проверьте соединение с интернетом, сервер не отвечает."
    }

    const status = error.response.status

    if (status >= 500) {
        return "Проблема на стороне сервера, мы уже работаем над ее устранением."
    }

    const data = error.response.data
    const text = isArray(data) ? data.join(',') : typeof data === 'string' || data.detail || data.message || data.error

    const answer = text || statusMessages[status]

    return answer
}

app.config.errorHandler = (err, vm, info) => {
    notify({
        type: 'warn',
        text: textOfError(err),
    })
}

window.addEventListener('unhandledrejection', event => {
    notify({
        type: 'error',
        text: textOfError(event.reason),
    })
});