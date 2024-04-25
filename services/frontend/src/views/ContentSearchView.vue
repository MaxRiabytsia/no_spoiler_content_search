<script setup>
import { ref, onMounted } from 'vue';
import SearchBar from "@/components/SearchBar.vue";

const lastWatchedEpisode = ref(null);

onMounted(() => {
  // Simulating fetching the last watched episode data from a script
  lastWatchedEpisode.value = {
    title: 'S1E1: Winter Is Coming',
    description: 'Eddard Stark is torn between his family and an old friend when asked to serve at the side of King Robert Baratheon. Viserys plans to wed his sister to a nomadic warlord in exchange for an army.',
    imageUrl: 'got_s1e1.jpeg'
  };
});

const getImgUrl = (pic) => {
  return require('../assets/' + pic)
}

</script>

<template>
  <div class="container">
    <div class="last-watched">
      <h3>Last Watched Episode:</h3>
      <div class="episode-info" v-if="lastWatchedEpisode">
        <div class="episode-image">
          <img :src="getImgUrl(lastWatchedEpisode.imageUrl)" alt="Episode Image" />
        </div>
        <div class="episode-details">
          <h4>{{ lastWatchedEpisode.title }}</h4>
          <p>{{ lastWatchedEpisode.description }}</p>
        </div>
      </div>
    </div>
    <div class="search-section">
      <h1>What content are you looking for?</h1>
      <div class="search-bar-container">
        <div class="dropdown-container">
          <select class="range-dropdown">
            <option value="" selected>Episode range</option>
          </select>
        </div>
        <div class="search-bar">
          <SearchBar @search="handleSearch"/>
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
}

.range-dropdown {
  appearance: none;
  color: rgba(255, 255, 255, 0.6);
  background-color: #222222;
  border: 2px solid #666666;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  outline: none;
  height: 52px;
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