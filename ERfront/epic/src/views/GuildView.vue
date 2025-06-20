<template>
    <div class="guild-hall">
        <h1 class="guild-title">Гильдия Авантюристов</h1>
        <div class="tab-buttons">
            <button @click="activeTab = 'quests'" :class="{ active: activeTab === 'quests' }">Задания</button>
            <button @click="activeTab = 'shop'" :class="{ active: activeTab === 'shop' }">Магазин</button>
        </div>
        <div class="quests-list" v-if="activeTab === 'quests'">
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
        <div v-if="activeTab === 'shop'" class="shop-grid">
            <div
                v-for="item in shopItems"
                :key="item.id"
                class="item-card"
                @click="openItemDetails(item)"
            >
                <img :src="item.image_url" alt="Иконка предмета" class="item-image"/>
                <p class="item-name">{{ item.name }}</p>
                <div class="item-cost">{{ item.gold_cost }}</div>
            </div>
        </div>
        <dialog ref="itemDialog" class="item-dialog">
            <div class="item-details">
                <img :src="selectedItem?.image_url" alt="Изображение предмета" class="dialog-image"/>
                <h3>{{ selectedItem?.name }}</h3>
                <p>{{ selectedItem?.description }}</p>
                <button @click="buyItem(selectedItem)"><span class="cost-tag">{{ selectedItem?.gold_cost }}</span></button>
                <button @click="$refs.itemDialog.close()">Отмена</button>
            </div>
        </dialog>
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
    name: 'GuildView',
    data(){
        return{
            quests:[],
            activeTab:'quests',
            selectedItem: null,
            shopItems: [
                {
                    "id": 1,
                    "name": "Клинок тьмы",
                    "description": "Увеличивает урон на 10%",
                    "type": "weapon",
                    "stats": { "strength": 5 },
                    "gold_cost": 200,
                    "image_url": "./src/assets/images/KT.png" 
                },
                {
                    "id": 2,
                    "name": "Посох мудрости",
                    "description": "+3 к интеллекту",
                    "type": "weapon",
                    "gold_cost": 150,
                    "image_url": "./src/assets/images/PM.png" 
                },
                {
                    "id": 3,
                    "name": "Зелье здоровья",
                    "description": "Восстанавливает 20 HP",
                    "type": "consumable",
                    "gold_cost": 50,
                    "image_url": "./src/assets/images/ZZ.png" 
                }
            ],
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
        },

        openItemDetails(item){
            this.selectedItem = item
            this.$refs.itemDialog.showModal()
        },

    }

}
</script>
