<script setup>
import { ref } from 'vue';
import SearchBar from "@/components/SearchBar.vue";
//import axios from 'axios';

const searchResults = ref([]);

const handleSearch = async (query) => {
  try {
    //const response = await axios.get(`http://your-api-url/search?query=${query}`);
    console.log('Searching for:', query);
    const response = {
      data: [
        { id: 1, name: 'Breaking Bad', description: 'A high school chemistry teacher turned methamphetamine producer' },
        {
          id: 2,
          name: 'Game of Thrones',
          description: 'Seven noble families fight for control of the mythical land of Westeros'
        },
        { id: 3, name: 'The Office', description: 'A mockumentary on a group of typical office workers' },
      ]
    };
    searchResults.value = response.data;
  } catch (error) {
    console.error('Error fetching search results:', error);
    searchResults.value = [];
  }
}
</script>

<template>
  <main>
    <h1>What show are you currently watching?</h1>
    <SearchBar @search="handleSearch"/>
    <div class="how-it-works">
      <h2>How does this work?</h2>
      <div class="steps">
        <div class="step">
          <div class="step-icon">
            <img src="@/assets/search-icon.png" alt="Search icon" />
          </div>
          <div class="step-content">
            <h3>Search for a TV Show</h3>
            <p>Start typing the name of a TV show you are currently watching, and then choose it from the appearing suggestions.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-icon">
            <img src="@/assets/last-episode-icon.png" alt="Last episode icon" />
          </div>
          <div class="step-content">
            <h3>Select the Last Episode You Have Seen</h3>
            <p>Once the show is found, you will see all its seasons and episodes. Choose the one you have seen last.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-icon">
            <img src="@/assets/search-content-icon.png" alt="Search content icon" />
          </div>
          <div class="step-content">
            <h3>Search for Content</h3>
            <p>Search for any YouTube videos you want to see. The release date of the video will not exceed the airing date of the next show episode. So you can be sure the video is spoiler-free!</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 16px;

  h1 {
    margin-bottom: 16px;
    text-align: center;
  }
}

.how-it-works {
  width: 100%;
  margin-top: 20px;

  h2 {
    margin-bottom: 16px;
    text-align: center;
  }

  .steps {
    display: flex;
    justify-content: center;
    gap: 16px;

    .step {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      text-align: left;
      background-color: #222222;
      border: 2px solid #666666;
      border-radius: 8px;
      padding: 24px;
      flex: 1;
      aspect-ratio: 6/1;

      .step-icon {
        margin-bottom: 16px;

        img {
          max-height: 60px;
        }
      }

      .step-content {
        h3 {
          margin-bottom: 8px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .how-it-works {
    .steps {
      flex-direction: column;
      align-items: center;
    }
  }
}
</style>