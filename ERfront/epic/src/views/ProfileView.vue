<template>
    <div class="profile-container">
        <h2>Профиль</h2>
        <div class="profile-info">
            <p><strong>ID:</strong> {{ user.id }}</p>
            <p><strong>Имя:</strong> {{ user.name }}</p>
            <p><strong>Выполнено задач:</strong> {{ user.completedTasks }}</p>
            <button @click="open = true">Открыть модальное окно</button>
            <div v-if="open" class="modal">
                <p>Привет из модального окна!</p>
                <button @click="open = false">Закрыть</button>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name:'ProfileView',
        data(){
            return{
                user:{
                    id: '',
                    name:'',
                    completedTasks:0
                },
                open:false
            }
        },
        async mounted(){
            await this.fetchProfile()
        },
        methods:{
            async fetchProfile(){
                try{
                    const tg_user = window.Telegram.WebApp.initDataUnsafe?.user 
					const response = await fetch(`http://127.0.0.1:8000/api/user/me/${tg_user.id}`)
					const data = await response.json()
                    this.user.id = tg_user.id
                    this.user.name = tg_user.first_name
                    this.user.completedTasks = data.completedTasks
                }catch(error){
                    console.log(error)
                }
            }
        }
    }
</script>

<style scoped>
.modal {
  background-color: aquamarine;
  position: fixed;
  z-index: 999;
  top: 20%;
  left: 50%;
  width: 300px;
  margin-left: -150px;
}
.profile-container{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 16px;
}

.profile-info{
    background-color: #ffffffcc;
    backdrop-filter: blur(8px);
    padding: 16px;
    border-radius: 8px;
    text-align: left;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    margin-top: 16px;
    width: 100%;
    max-width: 320px;
}
</style>