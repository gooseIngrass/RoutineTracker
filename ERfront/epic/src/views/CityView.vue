<template>
    <div class="city-container">
        <div class="quests-list">
			<div
				v-for="quest in quests"
				:key="quest.id"
				class="quest-item"
                @click="openQuestDetails(quest)"
			>
				<div class="quest-text">
					{{ quest.title }}
                    {{ quest.lvl_required }}
                    {{ quest.exp_reward }}
                    {{ quest.gold_reward }}
				</div>
			</div>
        </div>
        <dialog ref="questDialog">
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
                const response = await fetch(`http://127.0.0.1:8000/api/quests/${this.store.charId}`)
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
							char_id:this.store.charId, 
							field: 'active_quest',
                            value: 1
						})
					})
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

<style scoped>
.dialog-content {
  max-width: 400px;
}


.city-container{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 16px;
}

.quests-list{
	display: flex;
	flex-direction: column;
	gap: 8px;
}

.quest-item{
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: #ffffffcc;
	padding: 8px 12px;
	border-radius: 8px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.quest-text{
	font-size: 16px;
}

</style>