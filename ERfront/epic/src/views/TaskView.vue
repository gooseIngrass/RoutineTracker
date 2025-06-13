<template>
	<div class="tasks-container">
		<dialog ref="taskDialog">
			<form @submit.prevent="createTask">
				<h3>Добавить задачу</h3>

				<label>Название задачи:</label>
				<input type="text" v-model.trim="newTaskTitle" placeholder="Введите название" required />

				<label>Описание:</label>
				<textarea v-model.trim="newTaskDescription" placeholder="Введите описание"></textarea>

				<div class="difficulty-buttons">
				<button type="button" @click="newTaskDifficulty = 'LOW'" :class="{ active: newTaskDifficulty === 'LOW' }">Легко</button>
				<button type="button" @click="newTaskDifficulty = 'MEDIUM'" :class="{ active: newTaskDifficulty === 'MEDIUM' }">Нормально</button>
				<button type="button" @click="newTaskDifficulty = 'HIGH'" :class="{ active: newTaskDifficulty === 'HIGH' }">Сложно</button>
				</div>

				<!-- Кнопка создания -->
				<button type="submit" class="create-btn">Создать</button>
				<button type="button" @click="closeDialog">Отмена</button>
			</form>
		</dialog>
		<button @click="this.$refs.taskDialog.show()" class="add-button">+</button>

		<div class="tasks-list">
			<div
				v-for="task in tasks"
				:key="task.id"
				class="task-item"
			>
				<div class="task-text">
					{{ task.title }}
				</div>
				<button 
					class="complete-button"
					@click="completeTask(task.id)">Выполнено
				</button>
			</div>
		</div>
	</div>
</template>

<script>
	export default{
		name: 'TasksView',
		data(){
			return {
				tasks:[],
				newTaskTitle: '',
				newTaskDescription:'',
				newTaskDifficulty:'',
				charId:0
			}
		},

		async mounted(){
			await this.fetchTasks()
			try {
				const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
				const response = await fetch(`http://127.0.0.1:8000/api/user/character/${tg_user.id}`)
				const data = await response.json()

				const router = this.$router
				if (!data) {
					router.push('/welcome') 
				}
				this.charId = data.id
			}
			catch(error){
				console.log(error)
			}
		},
    

		methods:{
			async fetchTasks(){
				try{
					const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
					const response = await fetch(`http://127.0.0.1:8000/api/tasks/${tg_user.id}`)
					const data = await response.json()
					this.tasks = data
				} catch(error){
					console.log('error', error)
				}
			},
			async createTask(){
				if(!this.newTaskTitle) return

				try{
					const tg_user = window.Telegram.WebApp.initDataUnsafe?.user
					const response = await fetch(`http://127.0.0.1:8000/api/add`, {
						method: 'POST',
						headers:{
							'Content-Type': 'application/json'
						},

						body: JSON.stringify({ 
							tg_id:tg_user.id, 
							title: this.newTaskTitle,
							desc: this.newTaskDescription,
							diff: this.newTaskDifficulty 
						})

					})
					if (response.ok){
						this.newTask = ''
						await this.fetchTasks()
					}else {
						console.error('Ошибка', response.status)
					}
				}catch(error){
					console.log('Error', error)
				}
			},
			async completeTask(taskId){
				try{
					const response = await fetch(`http://127.0.0.1:8000/api/completed`, {
						method: 'PATCH',
						headers:{
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({ task_id:taskId, char_id:this.charId })
					})

					if (response.ok){
						await this.fetchTasks()
					}else {
						console.error('Ошибка', response.status)
					}
				}catch(error){
					console.log("error", error)
				}
			},
			closeDialog() {
				this.newTask = ''
				this.newTaskDescription = ''
				this.newTaskDifficulty = 'easy'
				this.$refs.taskDialog.close()
			}

		}
	}
</script>

<style scoped>
.tasks-container{
	flex: 1;
	display: flex;
	flex-direction: column;
	padding: 16px;
	overflow-y: auto;
}

.tasks-header{
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	margin-bottom: 16px;
}

.task-input{
	flex: 1;
	padding: 8px;
	font-size: 16px;
	border: 1px solid #ccc;
	border-radius: 8px;
	margin-right: 8px;
}

.add-button{
	background-color: #007aff;
	color: white;
	border: none;
	font-size: 24px;
	border-radius: 50%;
	cursor: pointer;
	outline: none;
	height: 40px;
	width: 40px;
}

.tasks-list{
	display: flex;
	flex-direction: column;
	gap: 8px;
}

.task-item{
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: #ffffffcc;
	padding: 8px 12px;
	border-radius: 8px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.task-text{
	font-size: 16px;
}

.complete-button{
	background-color: #4caf50;
	color: white;
	border: none;
	padding: 6px 12px;
	border-radius: 8px;
	cursor: pointer;
}

dialog {
  border-radius: 10px;
  padding: 20px;
  width: 300px;
}

.difficulty-buttons button {
  margin: 5px;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.difficulty-buttons button.active {
  background-color: #007BFF;
  color: white;
  border-color: #007BFF;
}

</style>