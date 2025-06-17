<template>
    <div class="guild-hall">
        <div class="quests-list">
			<div
				v-for="quest in quests"
				:key="quest.id"
				class="quest-item"
                @click="openQuestDetails(quest)"
			>
				<div class="quest-text">
					{{ quest.title }}
				</div>
                <div class="quest-details">
                    lvl: {{ quest.lvl_required }} <br/>
                    Награда: {{ quest.exp_reward }} exp, {{ quest.gold_reward }} g
                </div>
			</div>
        </div>
        <dialog ref="questDialog" class="quest-dialog">
            <div class="dialog-content">
                <h2>{{ selectedQuest.title }}</h2>
                <p>{{ selectedQuest.description }}</p>
                <p>Требуется уровень: {{ selectedQuest.lvl_required }}</p>
                <p>Награда: {{ selectedQuest.gold_reward }} золота, {{ selectedQuest.exp_reward }} опыта</p>
                <button @click="acceptQuest">Принять</button>
                <button @click="closeQuestDialog">Отмена</button>
            </div>
        </dialog>
    </div>
</template>

<script>
import { userStore } from '../../stores/userStore'
import '../assets/css/cityView.css'
export default{
    name: 'CityView',
    data(){
        return{
            quests:[],
            store: userStore(),
            selectedQuest: {}
        }
    },

    async mounted(){
        await this.fetchQuests()
    },

    methods:{
        async fetchQuests(){
            try{
                const response = await fetch(`http://127.0.0.1:8000/api/quests/${this.store.character.id}`)
				const data = await response.json()
                this.quests = data
            } catch(error){
                console.log(error)
            }
        },

        async acceptQuest(){
            try{
                const response = await fetch(`http://127.0.0.1:8000/api/user/character/update`,{
						method: 'PATCH',
						headers:{
							'Content-Type': 'application/json'
						},

						body: JSON.stringify({ 
							char_id:this.store.character.id, 
							field: 'active_quest',
                            value: this.selectedQuest.id
						})
					})
                this.store.selectedQuest = this.selectedQuest
                if(response.ok){
                    console.log('Квест взят')
                }
            }catch(error){
                console.log(error)
            }
        },

        openQuestDetails(quest){
            this.$refs.questDialog.show()
            this.selectedQuest = quest

        },

        closeQuestDialog(){
            this.selectedQuest.value = null
            this.$refs.questDialog.close()
        }
    }

}
</script>
