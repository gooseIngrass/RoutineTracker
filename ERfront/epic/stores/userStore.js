import { defineStore } from "pinia";

export const userStore = defineStore('user',{
    state: () =>({
        tg_user: '',
		character:{},
        selectedQuest:{}
    }),

    actions:{
		async updateChar(char_id, field, value){
			try{
				const response = await fetch(`http://127.0.0.1:8000/api/user/character/update`,{
						method: 'PATCH',
						headers:{
							'Content-Type': 'application/json'
						},
	
						body: JSON.stringify({ 
							char_id: char_id, 
							field: field,
							value: value
						})
				})
	
				if(response.ok){
					console.log(`Поле ${field} обновлено`)
				}
			}catch(error){
				console.log(error)
			}
		},

        async fetchChar(){
            try {
				const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
				const response = await fetch(`http://127.0.0.1:8000/api/user/character/${tg_user.id}`)
				const data = await response.json()

				const router = this.$router
				if (!data) {
					router.push('/welcome') 
				}
				console.log(data)
				this.character = data
			}
			catch(error){
				console.log(error)
			}
        },

        async fetchQuest(){
            try {
				const response = await fetch(`http://127.0.0.1:8000/api/user/character/${this.character.id}/quest`)
				const data = await response.json()
                this.selectedQuest = data
                console.log(data)
			}
			catch(error){
				console.log(error)
			}
        }
        
    }
})