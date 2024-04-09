<script setup>
import { ref, defineEmits } from "vue";

const emit = defineEmits(["search"]);
const searchQuery = ref('');

const search = () => {
  emit('search', searchQuery.value);
}
</script>

<template>
  <div class="input-wrap">
    <input type="text" v-model="searchQuery" @keydown.enter="search" />
    <button @click="search">Search</button>
  </div>
</template>

<style lang="scss" scoped>
.input-wrap {
  display: flex;
  transition: 250ms ease;
  border: 2px solid #090809;

  &:focus-within {
    box-shadow: 0 -4px 6px -1px rgb(0 0 0 / 0.1),
      0 -2px 4px -2px rgb(0 0 0 / 0.1);
  }

  input {
    width: 100%;
    padding: 8px 6px;
    border: none;
    background-color: #312D40;
    color: #ECECEC;

    &:focus {
      outline: none;
    }
  }

  button {
    padding: 8px 16px;
    border: none;
    background-color: #7AAE80;
    color: #090809;
  }
}
</style>