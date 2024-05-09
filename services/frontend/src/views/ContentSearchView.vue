<script setup>
import { ref, onMounted, computed } from 'vue';
import SearchBar from "@/components/SearchBar.vue";
import {useRoute} from "vue-router";
import { useStore } from 'vuex';

const lastWatchedEpisode = ref(null);
const route = useRoute();
const store = useStore();

onMounted(() => {
  lastWatchedEpisode.value = route.query;
  store.state.lastWatchedEpisode = route.query;
});

function getImgUrl(pic) {
  if (!pic) {
    return require('../assets/no_img.jpg');
  }

  return pic.startsWith("http") ? pic : require('../assets/' + pic);
}

const selectedRange = computed({
  get: () => store.state.selectedRange,
  set: (value) => store.commit('setSelectedRange', value),
});

</script>

<template>
  <div class="container">
    <div class="last-watched">
      <h3>Last Watched Episode:</h3>
      <div class="episode-info" v-if="lastWatchedEpisode">
        <div class="episode-image">
          <img :src="getImgUrl(lastWatchedEpisode.image_url)" alt="Episode Image" />
        </div>
        <div class="episode-details">
          <h4>{{ lastWatchedEpisode.name }}</h4>
          <p>{{ lastWatchedEpisode.description }}</p>
        </div>
      </div>
    </div>
    <div class="search-section">
      <h1>What content are you looking for?</h1>
      <div class="search-bar-container">
        <div class="dropdown-container">
          <select class="range-dropdown" v-model="selectedRange">
            <option value="" class="default-option" selected>Episode range</option>
            <option value="show_start">Show Start - This Episode</option>
            <option value="season_start">Season Start - This Episode</option>
            <option value="prev_ep">Previous Episode - This Episode</option>
          </select>
        </div>
        <div class="search-bar">
          <SearchBar route-name="content_results" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #222222;
  color: #FFFFFF;
}

.last-watched {
  margin-bottom: 40px;
}

.last-watched h3 {
  margin-bottom: 20px;
  text-align: left;
}

.episode-info {
  display: flex;
  align-items: flex-start;
}

.episode-image {
  flex: 0 0 350px;
  margin-right: 20px;
}

.episode-image img {
  width: 100%;
  height: auto;
}

.episode-details {
  text-align: left;
}

.episode-details h4 {
  margin-bottom: 10px;
}

.search-section {
  margin-bottom: 20px;
}

.search-section h1 {
  color: #FFFFFF;
  margin-bottom: 10px;
  text-align: center;
}

.search-bar-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.dropdown-container {
  position: relative;
  display: inline-block;
  margin-right: 10px;
  color: #FFFFFF;
}

.range-dropdown {
  appearance: none;
  background-color: #222222;
  border: 2px solid #666666;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  outline: none;
  height: 52px;
  color: #FFFFFF;
}

.default-option {
  color: rgba(255, 255, 255, 0.6);
}

.dropdown-container::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid #2d9c5e;
  pointer-events: none;
}

.search-bar {
  flex: 0 0 500px;
}
</style>