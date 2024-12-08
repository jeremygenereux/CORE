import { defineStore } from 'pinia';

const playerLineStructure = {
    playerId: null,
    firstName: '',
    lastName: '',
    number: null,
    position: '',
    lineId: null,
};

const lineStructure = {
    lineId: null,
    lineNum: null,
    isOffense: null,
};

export const useLinesStore = defineStore('lines', {
    state: () => ({
        lines: [],
        playersLines: [],
    }),
    actions: {
        removePlayerFromLine(playerId){
            const player = this.playersLines.find(playerLine => playerLine.playerId === playerId);
            if (player) {
                player.lineId = null;
            } else {
                console.error(`Player with id ${playerId} not found`);
            }
        },
        addPlayerToLine(playerId, lineId) {
            const player = this.playersLines.find(playerLine => playerLine.playerId === playerId);
            if (player) {
                player.lineId = lineId;
            } else {
                console.error(`Player with id ${playerId} not found`);
            }
        },
        clearLines() {
            this.lines = [];
        },
        clearPlayersLines() {
            this.playersLines = [];
        },
        clearAll() {
            this.clearLines();
            this.clearPlayersLines();
        }
    },
    persist: true,
});