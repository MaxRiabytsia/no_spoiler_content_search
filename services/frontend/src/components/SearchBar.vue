<script setup>
import { ref, defineEmits } from "vue";

const emit = defineEmits(["search"]);
const searchQuery = ref('');

const search = () => {
  emit('search', searchQuery.value);
}
</script>

<template>
  <div class="search-bar">
    <input type="text" v-model="searchQuery" @keydown.enter="search" placeholder="Search" />
    <button @click="search" class="search-button">
      <img src="@/assets/search-icon.png" alt="Search icon" />
    </button>
  </div>
</template>

<style lang="scss" scoped>
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