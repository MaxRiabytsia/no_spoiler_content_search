<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router'
import axios from 'axios'


const route = useRoute();
const showData = ref({});
const episodes = ref([]);
const selectedSeason = ref(1);
const selectedEpisodeId = ref(null);


onMounted(() => {
  const searchQuery = route.query.q
  axios.get(`http://localhost:5000/show_data?title=${searchQuery}`)
    .then(response => {
      showData.value = response.data[0]
      episodes.value = response.data[1]
      console.log(response.data)
    })
    .catch(error => {
      console.error(error)
    })
})

function selectEpisode(episodeId) {
  selectedEpisodeId.value = episodeId;
}

function getImgUrl(pic) {
  return require('../assets/' + pic);
}
</script>

<template>
  <div class="episodes-view">
    <div class="show-info">
      <img :src="showData.image_url" :alt="showData.title" class="show-poster"/>
      <div class="show-details">
        <h2>{{ showData.title }}</h2>
        <p>{{ showData.description }}</p>
      </div>
    </div>
    <h1>What was the last episode you have seen?</h1>
    <div class="last-episode">
      <div class="dropdown-container">
        <select v-model="selectedSeason" @change="fetchEpisodes" class="season-dropdown">
          <option v-for="season in showData.seasons" :key="season.id" :value="season.id">
            {{ season.name }}
          </option>
        </select>
      </div>
      <div class="episodes">
        <div
            v-for="episode in episodes"
            :key="episode.id"
            class="episode-card"
            :class="{ selected: episode.id === selectedEpisodeId }"
            @click="selectEpisode(episode.id)"
        >
          <img :src="getImgUrl(episode.imageUrl)" :alt="episode.title" class="episode-thumbnail"/>
          <div class="episode-details">
            <h4>{{ episode.title }}</h4>
            <p>{{ episode.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.episodes-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.show-info {
  display: flex;
  align-items: flex-start;
  margin-bottom: 2rem;
  max-width: 1200px;
  width: 100%;
}

.show-poster {
  max-width: 200px;
  margin-right: 1rem;
}

.show-details {
  margin-top: 0;
  text-align: left;
}

.last-episode {
  width: 100%;
  max-width: 1200px;
  text-align: left;
}

.dropdown-container {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.season-dropdown {
  appearance: none;
  background-color: #222222;
  color: #ffffff;
  border: 2px solid #666666;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  outline: none;
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

.episodes {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  justify-items: center;
  max-width: 1200px;
  width: 100%;
}

.episode-card {
  background-color: #222222;
  border: 2px solid #666666;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

.episode-card.selected {
  border-color: #2d9c5e;
}

.episode-thumbnail {
  max-width: 100%;
  height: auto;
}

.episode-details {
  margin-top: 0.5rem;
}
</style>