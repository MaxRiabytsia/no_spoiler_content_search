<script>
export default {
  data() {
    return {
      showData: {
        title: 'Game of Thrones',
        description: 'Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.',
        imageUrl: 'https://cdn.europosters.eu/image/1300/art-photo/game-of-thrones-season-1-key-art-i135455.jpg',
        seasons: [
          {id: 1, name: 'Season 1'},
          {id: 2, name: 'Season 2'},
        ],
      },
      selectedSeason: 1,
      episodes: [],
      selectedEpisodeId: null,
    };
  },
  created() {
    this.fetchEpisodes();
  },
  methods: {
    fetchEpisodes() {
      this.episodes = [
        {
          id: 1,
          title: 'Episode 1: Winter Is Coming',
          description: 'Eddard Stark is torn between his family and an old friend when asked to serve at the side of King Robert Baratheon. Viserys plans to wed his sister to a ...',
          imageUrl: 'got_s1e1.jpeg',
        },
        {
          id: 2,
          title: 'Episode 2: The Kingsroad',
          description: 'While Bran recovers from his fall, Ned takes only his daughters to King\'s Landing. Jon Snow goes with his uncle Benjen to the Wall. Tyrion joins them.',
          imageUrl: 'got_s1e2.jpeg',
        },
        {
          id: 3,
          title: 'Episode 3: Lord Snow',
          description: 'Jon begins his training with the Night\'s Watch; Ned confronts his past and future at King\'s Landing; Daenerys finds herself at odds with Viserys.',
          imageUrl: 'got_s1e3.jpeg',
        },
        {
          id: 4,
          title: 'Episode 4: Cripples, Bastards, and Broken Things',
          description: 'Eddard investigates Jon Arryn\'s murder. Jon befriends Samwell Tarly, a coward who has come to join the Night\'s Watch.',
          imageUrl: 'got_s1e4.jpeg',
        },
        {
          id: 5,
          title: 'Episode 1: Winter Is Coming',
          description: 'Eddard Stark is torn between his family and an old friend when asked to serve at the side of King Robert Baratheon. Viserys plans to wed his sister to a ...',
          imageUrl: 'got_s1e1.jpeg',
        },
        {
          id: 6,
          title: 'Episode 2: The Kingsroad',
          description: 'While Bran recovers from his fall, Ned takes only his daughters to King\'s Landing. Jon Snow goes with his uncle Benjen to the Wall. Tyrion joins them.',
          imageUrl: 'got_s1e2.jpeg',
        },
        {
          id: 7,
          title: 'Episode 3: Lord Snow',
          description: 'Jon begins his training with the Night\'s Watch; Ned confronts his past and future at King\'s Landing; Daenerys finds herself at odds with Viserys.',
          imageUrl: 'got_s1e3.jpeg',
        },
        {
          id: 8,
          title: 'Episode 4: Cripples, Bastards, and Broken Things',
          description: 'Eddard investigates Jon Arryn\'s murder. Jon befriends Samwell Tarly, a coward who has come to join the Night\'s Watch.',
          imageUrl: 'got_s1e4.jpeg',
        },
      ];
    },
    selectEpisode(episodeId) {
      this.selectedEpisodeId = episodeId;
    },
    getImgUrl(pic) {
      return require('../assets/' + pic)
    }
  }
};
</script>

<template>
  <div class="episodes-view">
    <div class="show-info">
      <img :src="showData.imageUrl" :alt="showData.title" class="show-poster"/>
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

<style lang="scss" scoped>
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