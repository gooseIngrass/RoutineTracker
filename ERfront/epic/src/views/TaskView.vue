<template>
	<div class="tasks-container">
		<div class="tasks-list">
			<div
				v-for="task in tasks"
				:key="task.id"
				class="task-item"
			>
				<div class="task-text" @click="openTaskDetails(task)">
					{{ task.title }}
				</div>
				<button 
					class="complete-button"
					@click="completeTask(task.id)">Выполнено
				</button>
			</div>
		</div>
		<dialog ref="detailsDialog">
			<div class="details-dialog-container">
				<h3>{{ selectedTask.title }}</h3>
				<p class="details-dialog-description" v-if="selectedTask.description">{{ selectedTask.description }}</p>
				<button @click="this.$refs.detailsDialog.close()" type="button">Закрыть</button>
			</div>
		</dialog>


		<dialog ref="taskDialog">
			<form @submit.prevent="createTask">
				<div class="task-dialog-container">
					<h3>Мне нужно</h3>

					<input type="text" v-model.trim="newTaskTitle" placeholder="Заголовок" required />

					<textarea v-model.trim="newTaskDescription" placeholder="Напишите сюда что-нибудь"></textarea>

					<div class="difficulty-buttons">
						<button type="button" @click="newTaskDifficulty = 'LOW'" :class="{ active: newTaskDifficulty === 'LOW' }">Легко</button>
						<button type="button" @click="newTaskDifficulty = 'MEDIUM'" :class="{ active: newTaskDifficulty === 'MEDIUM' }">Нормально</button>
						<button type="button" @click="newTaskDifficulty = 'HIGH'" :class="{ active: newTaskDifficulty === 'HIGH' }">Сложно</button>
					</div>

					<!-- Кнопка создания -->
					<div class="create-btn">
						<button type="submit" @click="this.$refs.taskDialog.close()">ОК</button>
						<button type="button" @click="closeDialog">Отмена</button>
					</div>
				</div>
			</form>
		</dialog>
		
		<button @click="this.$refs.taskDialog.show()" class="add-button">+</button>
	</div>
</template>

<script>
	import { userStore } from '../../stores/userStore'
	import '../assets/css/taskView.css'
	export default{
		name: 'TasksView',
		data(){
			return {
				tasks:[],
				newTaskTitle: '',
				newTaskDescription:'',
				newTaskDifficulty:'',
				store: userStore(),
				selectedTask:{}
			}
		},

		async mounted(){
			await this.fetchTasks()
			await this.store.fetchChar()
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
						body: JSON.stringify({ task_id:taskId, char_id: this.store.character.id })
					})

					if (response.ok){
						await this.fetchTasks()
						await this.store.fetchChar()
					}else {
						console.error('Ошибка', response.status)
					}
				}catch(error){
					console.log("error", error)
				}
			},
			closeDialog() {
				this.newTaskTitle = ''
				this.newTaskDescription = ''
				this.newTaskDifficulty = 'easy'
				this.$refs.taskDialog.close()
			},

			openTaskDetails(task){
				this.$refs.detailsDialog.show()
				this.selectedTask = task
			}

		}
	}
</script>
