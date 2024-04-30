<script setup>
import { ref, computed } from "vue";
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('');

const search = () => {
  router.push({ name: 'episodes', query: { q: searchQuery.value } })
}

const clearSearch = () => {
  searchQuery.value = '';
}

const showClearButton = computed(() => {
  return searchQuery.value.length > 0;
});
</script>

<template>
  <div class="search-bar">
    <input type="text" v-model="searchQuery" @keydown.enter="search" placeholder="Search" />
    <button v-if="showClearButton" @click="clearSearch" class="clear-button">
      <img src="@/assets/clear-icon.png" alt="Clear icon" />
    </button>
    <div class="separator" v-if="showClearButton"></div>
    <button @click="search" class="search-button">
      <img src="@/assets/search-icon.png" alt="Search icon" />
    </button>
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  max-width: 500px;
  width: 100%;
  margin-bottom: 40px;
  border: 2px solid #666666;
  border-radius: 6px;
  overflow: hidden;

  input {
    flex: 1;
    padding: 12px;
    background-color: #222222;
    color: #FFFFFF;
    border: none;

    &::placeholder {
      color: rgba(255, 255, 255, 0.6);
    }

    &:focus {
      outline: none;

      &::placeholder {
        color: transparent;
      }
    }
  }

  .clear-button {
    padding: 12px;
    background-color: #222222;
    border: none;
    cursor: pointer;

    img {
      width: 20px;
      height: 20px;
    }
  }

  .separator {
    width: 1px;
    height: 24px;
    background-color: #666666;
    margin: 0 8px;
  }

  .search-button {
    padding: 12px;
    background-color: #222222;
    border: none;
    cursor: pointer;

    img {
      width: 24px;
      height: 24px;
    }
  }
}
</style>