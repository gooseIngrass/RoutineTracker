<template>
    <div class="dungeon-container">
        <div v-if="!quest.id">
            <p>Вы еще не выбрали квест</p>
        </div>

        <div v-else-if="!roomResult">
            <p>Выберите дверь</p>
            <button v-for="n in 3" :key="n" @click="enterRoom(n)" class="room-button">
                Дверь {{ n }}
            </button>
        </div>
        
        <div v-else>
            <div class="battle-screen">
                <div style="display: flex; flex-direction: row;">
                    <div class="character">
                        <img :src="roomResult.player.avatar_url" alt="Персонаж" width="100" />
                        <p>{{ userStore.character.name }}</p>
                        <div class="hp-bar-container">
                            <div class="hp-bar" :style="{ width: getHpPercentage(dungeonStore.battleState.playerHp) + '%' }"></div>
                        </div>
                    </div>

                    <div class="enemy">
                        <img :src="roomResult.enemy.avatar_url" alt="Монстр" width="100" />
                        <p>{{ roomResult.enemy.name }}</p>
                        <div class="hp-bar-container">
                            <div class="hp-bar enemy-bar" :style="{ width: getHpPercentage(roomResult.enemy.currentHp) + '%' }"></div>
                        </div>
                    </div>
                </div>
                <img src="../assets/images/molnia.png" width="20"/> {{ userStore.character.ap }}
                <div class="actions">
                    <div class="action-wrapper" v-for="action in battleActions" :key="action">
                        <span class="ap-cost">{{ getApCost(action) }}</span>
                        <button
                        @click="performAction(action)"
                        :disabled="dungeonStore.finished || userStore.character.ap < getApCost(action)"
                        >
                        {{ action }}
                        </button>
                    </div>
                </div>
                <div class="log" v-if="dungeonStore.battleState.log.length > 0">
                    <ul>
                        <li v-for="(log, index) in dungeonStore.battleState.log" :key="index">{{ log }}</li>
                    </ul>
                </div>

                <div v-if="dungeonStore.battleState.finished" class="result">
                    <p v-if="dungeonStore.battleState.result === 'win'" style="color: green;">🎉 Победа! Вы получили награду.</p>
                    <p v-else style="color: red;">💀 Вы проиграли. Попробуйте снова.</p>
                    <button @click="resetBattle">Вернуться</button>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import { userStore } from '../../stores/userStore'
import { dungeonStore } from '../../stores/dungeonStore'
import '../assets/css/dungeonView.css'
export default{
    data(){
        return{
            userStore: userStore(),
            dungeonStore: dungeonStore(),
            quest: {},
            battleActions:['Удар', 'Блок', 'Умение', 'Зелье'],
            roomResult: null, 
        }
    },

    async mounted(){
        await this.userStore.fetchQuest()
        this.quest = this.userStore.selectedQuest

        this.roomResult = this.dungeonStore.roomResult
    },

    async beforeUnmount(){//Синхронизируем значение AP с БД
        await this.userStore.updateChar(this.userStore.character.id, 'ap', this.userStore.character.ap)
        await this.userStore.updateChar(this.userStore.character.id, 'hp', this.userStore.character.hp)
        this.dungeonStore.roomResult = this.roomResult
    },

    methods:{
        getRandomEnemy(){
            const enemies = [
                { name: 'Гоблин', avatar_url: './src/assets/images/goblin.png', baseHp: 30 },
                { name: 'Скелет', avatar_url: './src/assets/images/skeleton.png', baseHp: 40 },
                { name: 'Огр', avatar_url: './src/assets/images/ogre.png', baseHp: 60 }
            ]
            const enemy = enemies[Math.floor(Math.random() * enemies.length)]
            return{
                ...enemy,
                currentHp: enemy.baseHp
            }
        },

        enterRoom(roomNumber){
            const resultTypes = ['treasure', 'trap', 'battle']
            const type = resultTypes[Math.floor(Math.random() * resultTypes.length)]
            
            if(type == 'battle'){
                const enemy = this.getRandomEnemy()
                this.roomResult = {
                    type: 'battle',
                    player:{
                        avatar_url:'./src/assets/images/knight.png'
                    },
                    enemy
                }
                console.log(this.roomResult)
                this.dungeonStore.initBattle()
            } else{
                this.roomResult = { type }
            }
        },

        log(msg){
            this.dungeonStore.addLog(msg)
        },

        //Действия игрока и моба
        performAction(action){
            if (this.dungeonStore.battleState.finished) return

            const enemy = this.roomResult.enemy

            switch(action){
                case 'Удар':
                    const damage = Math.floor(Math.random() * 10) + 5
                    enemy.currentHp -= damage
                    if(enemy.currentHp <= 0){
                        enemy.currentHp = 0
                    }
                    this.userStore.character.ap -= 2
                    this.log(`Вы ударили ${enemy.name} на ${damage} урона `)
                    break
                
                case 'Блок':
                    this.dungeonStore.battleState.playerDefence += 5
                    this.log('Вы поставили блок')
                    this.userStore.character.ap -= 1
                    break
                
                case 'Умение':
                    break

                case 'Зелье':
                    const heal = Math.floor(Math.random() * 15) + 10
                    this.dungeonStore.battleState.playerHp += heal
                    this.dungeonStore.battleState.playerDefence = 0
                    this.log(`Вы восстановили ${heal} HP`)
                    this.userStore.character.ap -= 1
                    break      
            }

            //Ход монстра
            if(enemy.currentHp > 0){
                const enemyDamage = Math.floor(Math.random() * 10) + 5
                const effectiveDamage = Math.max(enemyDamage - this.dungeonStore.battleState.playerDefence, 0)
                this.dungeonStore.battleState.playerHp -= effectiveDamage
                this.log(`${enemy.name} атаковал вас на ${effectiveDamage} урона`)
                this.dungeonStore.battleState.playerDefence = 0
            } else{
                //Проверяем окончание боя
                if (this.dungeonStore.battleState.playerHp <= 0) {
                    this.dungeonStore.battleState.result = 'lose'
                    this.log('Вы погибли...')
                }

                if (this.roomResult.enemy.currentHp <= 0) {
                    this.dungeonStore.battleState.result = 'win'
                    this.log('Вы победили!')
                }
                this.dungeonStore.battleState.finished = true
            }
        },

        resetBattle(){
            this.roomResult = null
            this.userStore.updateChar(this.userStore.character.id, 'exp', this.quest.exp_reward)
        },

        getApCost(action) {
            switch (action) {
            case 'Удар':
                return 2
            default:
                return 1
            }
        },

        getHpPercentage(currentHp) {
            const maxHp = this.roomResult.enemy?.baseHp || 100
            return Math.max((currentHp / maxHp) * 100, 0)
        }
    }

}
</script>
