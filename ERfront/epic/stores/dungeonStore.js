import { defineStore } from "pinia";

export const dungeonStore = defineStore('dungeon', {
    state: () => ({
        battleState:{
            playerHp: 50,
            enemyHp: 30,
            playerDefence: 0,
            finished: true,
            result: null,
            log: []
        },

        roomResult: null
    }),

    actions:{
        initBattle(){
            this.battleState = {
                playerHp: 50,
                enemyHp: 30,
                playerDefence: 0,
                finished: false,
                result: null,
                log: []
            }
        },

        addLog(message){
            this.battleState.log.push(message)
        }

    }
})