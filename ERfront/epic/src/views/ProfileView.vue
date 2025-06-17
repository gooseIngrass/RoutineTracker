<template>
    <div class="profile-container">
        <h1 class="profile-title">Профиль героя</h1>

        <div class="character-card">
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
        </div>
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
                character:{}
            }
        },
        async mounted(){
            this.character = this.store.character
        }
    }
</script>
