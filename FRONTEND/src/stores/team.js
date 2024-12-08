import { defineStore } from 'pinia';

const teamStructure = {
    id: null,
    coach_id: null,
    team_name: '',
    primary_color: '',
    secondary_color: '',
    logo: '',
    description: ''
};

export const useTeamStore = defineStore('team', {
    state: () => ({
        team: { ...teamStructure }
    }),
    actions: {
        chooseTeam(team) {
            this.team = team;
        },
        clearTeam() {
            this.team = null;
        }
    },
    persist: true,
});