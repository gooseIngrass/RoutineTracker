import { defineStore } from "pinia";

export const userStore = defineStore('user',{
    state: () =>({
        tg_user: '',
        charId: 0
    })
})