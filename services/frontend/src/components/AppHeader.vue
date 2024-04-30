<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <header>
    <nav class="container">
      <div class="branding">
        <RouterLink :to="{ name: 'search' }">
          <img src="@/assets/logo.png" alt="" />
        </RouterLink>
      </div>
      <ul class="nav-routes">
        <RouterLink :to="{ name: 'episodes' }">Episodes (temp)</RouterLink>
        <RouterLink :to="{ name: 'content_search' }">Content search (temp)</RouterLink>
        <RouterLink :to="{ name: 'content_results' }">Content results (temp)</RouterLink>
        <RouterLink :to="{ name: 'about' }">About</RouterLink>
      </ul>
    </nav>
  </header>
</template>

<style scoped>
header {
  font-size: 24px;
  background-color: #222222;
  color: #FFFFFF;
  border-bottom: 2px solid #666666;

  nav {
    display: flex;
    align-items: center;
    padding: 16px;

    .branding {
      display: flex;
      align-items: center;
      gap: 8px;

      img {
        max-width: 50px;
      }

      h1 {
        font-size: 24px;
      }
    }

    .nav-routes {
      display: flex;
      flex: 1;
      justify-content: flex-end;
      gap: 12px;
      list-style: none;

      a {
        text-decoration: none;
        color: inherit;
      }
    }
  }
}
</style>