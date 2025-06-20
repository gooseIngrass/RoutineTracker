<template>
    <div class="profile-container">
        <h1 class="profile-title">Профиль героя</h1>

        <div class="character-card">
            <button class="inventory-toggle" @click="toggleInventory">
                <img src="../assets/images/BP.png" alt="Инвентарь" />
                <img src="../assets/images/bronya.png" alt="Способности" />
                <img src="../assets/images/skill.png" alt="Снаряжение" width="64" height="64"/>
            </button>

            <h2>{{ character.name }} 
                <span class="level-badge">Уровень {{ character.level }}</span>
            </h2>

            <p><strong>Класс:</strong> {{ character.charClass }}</p>

            <div class="stat-block">
                <div class="stat-line">
                    <span class="stat-name">HP</span>
                    <span class="stat-value">{{ character.hp }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">AP</span>
                    <span class="stat-value">{{ character.ap }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">Золото</span>
                    <span class="stat-value">{{ character.gold }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">Опыт</span>
                    <span class="stat-value">{{ character.exp }}</span>
                </div>
            </div>

            <div class="stat-block">
                <h3>Характеристики</h3>
                <div class="stat-line">
                    <span class="stat-name">Сила</span>
                    <span class="stat-value">{{ character.strength }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">Интеллект</span>
                    <span class="stat-value">{{ character.intelligence }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">Выносливость</span>
                    <span class="stat-value">{{ character.constitution }}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">Восприятие</span>
                    <span class="stat-value">{{ character.perception }}</span>
                </div>
            </div>

            <div v-if="showInventory" class="inventory-container">
                <h3>Инвентарь</h3>
                <div class="inventory-grid">
                    <div
                    v-for="item in inventory"
                    :key="item.id"
                    class="inventory-item"
                    @click="openItemDetails(item)"
                    >
                        <img :src="item.image_url" :alt="item.name" width="24" height="30"/>
                    </div>
                </div>
            </div>
        </div>
        <dialog ref="itemDialog" class="item-dialog">
            <div class="item-details">
                <img :src="selectedItem?.image_url" class="dialog-image"/>
                <h3>{{ selectedItem?.name }}</h3>
                <p>{{ selectedItem?.description }}</p>
                <button @click="$refs.itemDialog.close()">Закрыть</button>
            </div>
        </dialog>
    </div>
</template>

<script>
    import '../assets/css/profileView.css'
    import { userStore } from '../../stores/userStore'
    export default{
        name:'ProfileView',
        data(){
            return{
                store:userStore(),
                showInventory: false,
                selectedItem: null,
                character:{},
                inventory: [
                    {
                        id: 1,
                        name: 'Клинок тьмы',
                        description: 'Меч, сделанный из чёрного железа',
                        stats: { strength: 5 },
                        image_url: './src/assets/images/KT.png' 
                    },
                    {
                        id: 2,
                        name: 'Посох мудрости',
                        description: 'Увеличивает интеллект на 5',
                        stats: { intelligence: 5 },
                        image_url: './src/assets/images/PM.png' 
                    },
                    {
                        id: 3,
                        name: 'Зелье здоровья',
                        description: 'Восстанавливает 20 HP',
                        stats: {},
                        image_url: './src/assets/images/ZZ.png' 
                    }
                ]
            }
        },

        async mounted(){
            this.character = this.store.character
        },

        methods: {
            toggleInventory(){
                this.showInventory = !this.showInventory
            },

            openItemDetails(item){
                this.selectedItem = item
                this.$refs.itemDialog.showModal()
            }
        }
    }
</script>
