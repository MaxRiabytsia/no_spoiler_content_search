<script setup>
import {onMounted, ref} from 'vue';
import SearchBar from "@/components/SearchBar.vue";
import axios from "axios";
import {useRoute} from "vue-router";
import {useStore} from 'vuex';


const videos = ref([]);
const route = useRoute();
const store = useStore();
const searchInfo = ref({
  show_title: store.state.showData.title,
  show_image_url: store.state.showData.image_url,
  episode_title: store.state.lastWatchedEpisode.name,
  episode_image_url: store.state.lastWatchedEpisode.image_url
});

onMounted(() => {
  const searchQuery = searchInfo.value.show_title + " " + route.query.q

  const end_id = store.state.lastWatchedEpisode.external_id
  let start_id = null
  const selectedRange = store.state.selectedRange
  const season = store.state.lastWatchedEpisode.season

  if (selectedRange === 'show_start') {
    start_id = store.state.allEpisodes[0].external_id
  } else if (selectedRange === 'prev_ep') {
    start_id = store.state.allEpisodes.find(
        episode => episode.number_in_show === store.state.lastWatchedEpisode.number_in_show - 1).external_id
  } else if (selectedRange === 'season_start') {
    start_id = store.state.allEpisodes.find(episode => episode.season === season &&
        episode.number_in_season === 1).external_id
  } else {
    start_id = store.state.allEpisodes[0].external_id
  }

  console.log(`http://localhost:5000/search_content?query=${searchQuery}&episode_range=${start_id}-${end_id}`)
  axios.get(`http://localhost:5000/search_content?query=${searchQuery}&episode_range=${start_id}-${end_id}`)
      .then(response => {
        console.log(response.data)
        videos.value = response.data
      })
      .catch(error => {
        console.error(error)
      })
})

const getImgUrl = (pic) => {
  return pic.startsWith("http") ? pic : require('../assets/' + pic);
}
</script>

<template>
  <div class="no-spoiler-search">
    <div class="content-container">
      <div class="show-info">
        <h2 class="show-name-title">TV Show:</h2>
        <p class="show-name">{{ searchInfo.show_title }}</p>
        <img :src="searchInfo.show_image_url" alt="" class="show-poster"/>
        <p class="last-watched-episode-title">Last Watched Episode:</p>
        <p class="last-watched-episode">{{ searchInfo.episode_title }}</p>
        <img :src="getImgUrl(searchInfo.episode_image_url)" alt="" class="show-poster"/>
      </div>
      <div class="main-content">
        <div class="search-container">
          <div class="dropdown-container">
            <select class="range-dropdown">
              <option value="" selected>Episode range</option>
              <option value="1">Season 1</option>
            </select>
          </div>
          <SearchBar route-name="content_results"/>
        </div>
        <div class="video-list">
          <div v-for="video in videos" :key="video.external_id" class="video-item">
            <a :href="video.url" class="video-url">
              <div class="video-item-content">
                <div class="thumbnail-container">
                  <img :src="getImgUrl(video.image_url)" :alt="video.title" class="thumbnail"/>
                </div>
                <div class="video-info">
                  <h3 class="video-title">{{ video.title }}</h3>
                  <p class="video-views">{{ video.channel_name }}</p>
                  <p class="video-description">{{ video.description }}</p>
                </div>
              </div>
            </a>
          </div>
        </div>
        <button class="load-more">Load more</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.no-spoiler-search {
  padding: 20px 200px 0 200px;
}

.content-container {
  display: flex;
}

.show-info {
  flex: 0 0 260px;
  padding-right: 50px;
  text-align: left;
}

.show-poster {
  width: 100%;
  height: auto;
  margin-bottom: 20px;
}

.show-name-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.show-name {
  font-size: 18px;
  margin-bottom: 10px;
  text-align: center;
}

.last-watched-episode-title {
  font-size: 18px;
  margin-bottom: 10px;
  padding-top: 10px;
  font-weight: bold;
  border-top: 1px solid #666666;
}

.last-watched-episode {
  font-size: 16px;
  margin-bottom: 10px;
  text-align: center;
}

.main-content {
  flex: 1;
}

.search-container {
  display: flex;
  align-items: flex-start;
}

.video-list {
  text-align: left;
}

.video-item {
  display: flex;
  align-items: flex-start;
  padding-top: 5px;
  padding-bottom: 5px;
}

.thumbnail-container {
  flex: 0 0 200px;
  margin-right: 20px;
}

.thumbnail {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.video-info {
  flex: 1;
  color: #cccccc;
}

.video-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #ffffff;
}

.video-views {
  font-size: 14px;
  margin-bottom: 10px;
}

.video-description {
  font-size: 14px;
}

.video-url {
  text-decoration: none;
  color: #ffffff;
}

.video-item-content {
  display: flex;
}

.load-more {
  display: block;
  margin: 40px auto 0;
  padding: 12px 24px;
  background-color: #222222;
  color: #FFFFFF;
  border: 2px solid #666666;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
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
  border-top: 8px solid #2D9C5E;
  pointer-events: none;
}
</style>