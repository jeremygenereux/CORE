// Store for the WebSocket connection. Even though the websocket instance is persisted, it is destroyed when
// the page is refreshed. Thus, whenever a page needs to have data from the websocket, it needs to connect to it
import { defineStore } from 'pinia';
import { usePlayersStatsStore } from "@/stores/playersStats.js";

export const useWebSocketStore = defineStore('webSocket', {
    state: () => ({
        websocket: null,
        isConnected: false,
        messages: [],
    }),
    actions: {
        connect() {
            const playersStatsStore = usePlayersStatsStore();
            if (this.websocket instanceof WebSocket) {
                console.log("WebSocket already connected");
            }
            else{
                console.log("WebSocket connecting");
                this.websocket = new WebSocket("ws://127.0.0.1:5000/ws");

                this.websocket.onopen = () => {
                    console.log("WebSocket connected");
                    this.isConnected = true;
                };

                this.websocket.onmessage = (event) => {
                    console.log("Message received from websocket:", event.data);
                    this.messages.push(event.data); // Store messages if needed
                    // Update player stats
                    const playerStat = JSON.parse(event.data);
                    playersStatsStore.updatePlayerStat(playerStat.playerId, playerStat);
                };

                this.websocket.onclose = () => {
                    console.log("WebSocket disconnected");
                    this.isConnected = false;
                    this.websocket = null; // Reset websocket instance on close
                };

                this.websocket.onerror = (error) => {
                    console.error("WebSocket error:", error);
                };
            }
        },
        disconnect() {
            if (this.websocket instanceof WebSocket) {
                this.websocket.close();
            }
            this.websocket = null;
            this.isConnected = false;
        },
        sendMessage(message) {
            if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
                this.websocket.send(message);
            } else {
                console.error("WebSocket is not open. Ready state: ", this.websocket.readyState);
            }
        },
    },
    persist: true,
});