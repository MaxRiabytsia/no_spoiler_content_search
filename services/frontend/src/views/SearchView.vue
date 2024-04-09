<script setup>
import SearchBar from "@/components/SearchBar.vue";
</script>

<template>
  <main>
    <h1>What show are you currently watching?</h1>
    <SearchBar />
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