// src/store/index.js
import {createStore} from 'vuex';

const store = createStore({
    state: {
        showData: {},
        allEpisodes: [],
        lastWatchedEpisode: {},
        selectedRange: "",
    },
    mutations: {
        setSelectedRange(state, value) {
      state.selectedRange = value;
    }
    },
});

export default store;