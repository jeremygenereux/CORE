import { defineStore } from 'pinia';

const hrHistoryStructure = {
    playerId: null,
    hr: []
}

export const useHrHistoryStore = defineStore('hrHistory', {
    state: () => ({
        hrHistory: []
    }),
    actions: {
        createHrHistory(playerIdList) {
            playerIdList.forEach(playerId => {
                this.hrHistory.push({  playerId: playerId, hr: [] });
            });
        },
        addHr(playerId, hr) {
            const index = this.hrHistory.findIndex(hr => hr.playerId === playerId);
            if (index !== -1) {
                this.hrHistory[index].hr.push(hr);
                if (this.hrHistory[index].hr.length > 20) {
                    this.hrHistory[index].hr.shift();
                }
            }
            else {
                this.hrHistory.push({ ...hrHistoryStructure, playerId, hr: [hr] });
            }
            console.log(`Added HR for player ${playerId}: ${this.hrHistory[index]?.hr}`);
        },
        clearHrHistory() {
            this.hrHistory = [];
        },
        getHrHistory(playerId) {
            const index = this.hrHistory.findIndex(hr => hr.playerId === playerId);
            return this.hrHistory[index]?.hr;
        }
    },
    persist: true,
})