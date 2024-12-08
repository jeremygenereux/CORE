import { defineStore } from 'pinia';

const playerStructure = {
    id: null,
    firstName: '',
    lastName: '',
    birthDate: '',
    email: '',
    number: null,
    position: '',
    maxHR: null,
    restHR: null,
    deviceId: '',
    deviceStatus: '',
};

export const usePlayersStore = defineStore('players', {
    state: () => ({
        players: []
    }),
    actions: {
        addPlayer(player) {
            this.players.push({ ...playerStructure, ...player });
        },
        updatePlayer(playerId, updatedPlayer) {
            console.log('updatePlayer', playerId, updatedPlayer);
            const index = this.players.findIndex(player => player.id === playerId);
            if (index !== -1) {
                this.players[index] = { ...this.players[index], ...updatedPlayer };
            }
            else{
                console.error('Player not found');
            }
        },
        clearPlayers() {
            this.players = [];
        }
    },
    persist: true,
});