<script setup>
import QRCodeStyling from "qr-code-styling";
import useProfileStore from '@/stores/profileStore'
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';

const profileStore = useProfileStore()
const { otp_uri, thisCanBeAddAndChanged } = storeToRefs(profileStore)
const code = ref(null)

onMounted(async () => {
    document.getElementById("qrcode").innerHTML = ""

    new QRCodeStyling({
        width: 200,
        height: 200,
        data: otp_uri.value,
        dotsOptions: {
            color: "#000000",
            type: "square"
        },
        backgroundOptions: {
            color: "#ffffff"
        }
    }).append(document.getElementById("qrcode"))
})

async function otp() {
    const r = await profileStore.otp_login(code.value)
}

</script>
<template>
    <div class="mycontainer">
        <div class="objectsView" style="margin: 0 auto;">
            <h3>
                Привяжите свой телефон к аккаунту по QR-коду
            </h3>
            <div id="qrcode" />
            <div class="objectsView" v-if="!thisCanBeAddAndChanged">
                <h3>
                    Или ведите код для доступа к администрированию данных
                </h3>

                <input type="text" v-model="code" class="form-control" placeholder="Ведите ваш код" maxlength="6" />
                <button class="btn btn-outline-secondary" type="button" @click="otp()">Ввести код</button>
            </div>
            <div v-else>
                <h3>
                    Вы успешно подтвердили свой аккаунт
                </h3>
            </div>

        </div>

    </div>
</template>