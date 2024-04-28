<script setup>
import { ref } from 'vue';
import SearchBar from "@/components/SearchBar.vue";

const showInfo = ref({
  title: 'Game of Thrones',
  lastWatched: 'S1E1 Winter Is Coming',
  episodeImage: 'got_s1e1.jpeg',
  showImage: 'https://cdn.europosters.eu/image/1300/art-photo/game-of-thrones-season-1-key-art-i135455.jpg',
});

const videos = ref([
  {
    id: 1,
    title: 'Ned | GOT REVIEW (Season 1)',
    views: '473,141',
    description: 'this video now has CLOSED CAPTIONS because the audio balancing is sorta bad.',
    channel: 'Glidus',
    thumbnail: 'glidus1.jpg',
  },
  {
    id: 2,
    title: 'Jon & Tyrion | GOT REVIEW (Season 1)',
    views: '211,561',
    description: 'Remember Season 1 of that one show? Remember the funny dwarf and the hot sad guy? Remember when Gildus used to make videos? Well, this video is gonna be a total nostalgia trip.',
    channel: 'Glidus',
    thumbnail: 'glidus2.jpg',
  },
  {
    id: 3,
    title: 'Daenerys | GOT REVIEW (Season 1)',
    views: '250,586',
    description: 'Wow, angry dragon lady had humble beginnings? Who knew. I hope you enjoyed the eyes. I\'ll look way too long. I look forward to doing it again.',
    channel: 'Glidus',
    thumbnail: 'glidus3.jpg',
  },
  {
    id: 4,
    title: 'Arya | GOT REVIEW (Season 1)',
    views: '254,361',
    description: 'thank you for waiting :) arya was a good character once so let\'s figure out why I guess',
    channel: 'Glidus',
    thumbnail: 'glidus4.jpg',
  },
]);

const selectedSeason = ref('');
const searchQuery = ref('');

const searchVideos = (query) => {
  searchQuery.value = query;
  // Implement video search logic based on the query
};

const getImgUrl = (pic) => {
  return require('../assets/' + pic)
}
</script>
<template>
  <div class="no-spoiler-search">
    <div class="content-container">
      <div class="show-info">
        <h2 class="show-name-title">TV Show:</h2>
        <p class="show-name">{{ showInfo.title }}</p>
        <img :src="showInfo.showImage" alt="" class="show-poster" />
        <p class="last-watched-episode-title">Last Watched Episode:</p>
        <p class="last-watched-episode">{{ showInfo.lastWatched }}</p>
        <img :src="getImgUrl(showInfo.episodeImage)" alt="" class="show-poster" />
      </div>
      <div class="main-content">
        <div class="search-container">
          <div class="dropdown-container">
            <select class="range-dropdown" v-model="selectedSeason">
              <option value="" selected>Episode range</option>
              <option value="1">Season 1</option>
            </select>
          </div>
          <SearchBar @search="searchVideos" />
        </div>
        <div class="video-list">
          <div v-for="video in videos" :key="video.id" class="video-item">
            <div class="thumbnail-container">
              <img :src="getImgUrl(video.thumbnail)" :alt="video.title" class="thumbnail" />
            </div>
            <div class="video-info">
              <h3 class="video-title">{{ video.title }}</h3>
              <p class="video-views">{{ video.channel }} | {{ video.views }} views</p>
              <p class="video-description">{{ video.description }}</p>
            </div>
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