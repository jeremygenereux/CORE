import { defineStore } from 'pinia';
import { useHrHistoryStore } from "@/stores/hrHistory.js";

const playerStatStructure = {
    playerId: null,
    firstName: '',
    lastName: '',
    number: null,
    lineNum: null,
    isOffense: null,
    hr: null,
    state: '',
    recScore: null,
};

export const usePlayersStatsStore = defineStore('playersStats', {
    state: () => ({
        playersStats: []
    }),
    actions: {
        addPlayerStat(playerStat) {
            this.playersStats.push({ ...playerStatStructure, ...playerStat });
        },
        updatePlayerStat(playerId, updatedPlayerStat) {
            const index = this.playersStats.findIndex(playerStat => playerStat.playerId === playerId);
            if (index !== -1) {
                const hrHistoryStore = useHrHistoryStore();
                this.playersStats[index].hr = updatedPlayerStat.hr;
                this.playersStats[index].state = updatedPlayerStat.state;
                this.playersStats[index].recScore = updatedPlayerStat.recScore;
                console.log(`Updated player ${playerId}: ${updatedPlayerStat}`);
                hrHistoryStore.addHr(playerId, updatedPlayerStat.hr);
            }
            else{
                console.warn(`Cannot update player, id ${playerId} not found;`)
                console.log('Player stats:', JSON.stringify(this.playersStats, null, 2));
            }
        },
        clearPlayersStats() {
            this.playersStats = [];
        }
    },
    persist: true,
});