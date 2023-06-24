import { create } from 'zustand';
import { persist } from "zustand/middleware";
import api from './utils/api';


export const useStore = create(persist(
    (set, get) => ({

        sidebarOpen: false,
        setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),

        view: "login",
        setView: (view) => set({ view }),

        apiToken: null,
        setApiToken: (apiToken) => set({ apiToken }),

        building: null,
        updateBuilding: (key, value) => {
            const { building } = get();
            let newBuilding;

            if (building === null) {
                newBuilding = {};
            } else {
                newBuilding = { ...building };
            }

            newBuilding[key] = value;
            set({ building: newBuilding });

        },

        amenities: [],
        getAmenities: async () => {
            const [response, statusCode] = await api.get("/api/v1/amenities");
            set({ amenities: response.results });
        },

        buildings: [],
        getBuildings: async () => {

            const [response, statusCode] = await api.get("/api/v1/buildings");
            set({ buildings: response.results });

        },



    }),
    {
        name: "peppermint-mini-11"
    }
));
