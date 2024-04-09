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
        { id: 2, name: 'Game of Thrones', description: 'Seven noble families fight for control of the mythical land of Westeros' },
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
    <SearchBar @search="handleSearch" />
    <h2>Search Results</h2>
    <ul v-if="searchResults.length">
      <li v-for="result in searchResults" :key="result.id">
        {{ result.name }} - {{ result.description }}
      </li>
    </ul>
    <div v-else>
      No results found.
    </div>
  </main>
</template>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: column;
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 16px;

  h1 {
    margin-bottom: 16px;
    text-align: center;
  }
}
</style>