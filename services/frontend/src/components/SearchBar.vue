<script setup>
import { ref, computed, defineProps, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const searchQuery = ref('');
const suggestions = ref([]);

const props = defineProps({
  routeName: {
    type: String,
    required: true,
  },
  enableAutocomplete: {
    type: Boolean,
    default: false,
  },
});


const fetchSuggestions = async () => {
  if (props.enableAutocomplete && searchQuery.value.length > 0) {
    const response = await fetch(`http://localhost:5000/search_suggestions?query=${encodeURIComponent(searchQuery.value)}`);
    suggestions.value = await response.json();
    // Sort suggestions to show items with images first
    suggestions.value.sort((a, b) => (b.image_url ? 1 : 0) - (a.image_url ? 1 : 0));
    // Remove duplicate names from suggestions
    suggestions.value = [...new Set(suggestions.value.map(suggestion => suggestion.title))].map(title => suggestions.value.find(suggestion => suggestion.title === title));
    // take first 5 suggestions
    let last_suggestion_number = suggestions.value.length < 5 ? suggestions.value.length : 5;
    suggestions.value = suggestions.value.slice(0, last_suggestion_number);
    await nextTick();
    console.log(suggestions.value)
  } else {
    suggestions.value = [];
  }
};

watch(searchQuery, fetchSuggestions);


const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion.title;
  suggestions.value = [];
  search();
};

const search = () => {
  router.push({ name: props.routeName, query: { q: searchQuery.value } })
}

const clearSearch = () => {
  searchQuery.value = '';
}

const showClearButton = computed(() => {
  return searchQuery.value.length > 0;
});

function getImgUrl(pic) {
  if (!pic) {
    return require('../assets/no_img.jpg');
  }

  return pic.startsWith("http") ? pic : require('../assets/' + pic);
}
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
    <div class="suggestions" v-show="suggestions.length > 0" :key="suggestions.join('-')">
      <ul>
        <li v-for="suggestion in suggestions" :key="suggestion.title" @click="selectSuggestion(suggestion)">
          <img :src="suggestion.image_url || getImgUrl('no_img.jpg')" :alt="suggestion.title" />
          <span>{{ suggestion.title }}</span>
        </li>
      </ul>
    </div>
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
  position: relative;

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

  .suggestions {
    position: absolute;
    top: calc(100% + 2px);
    left: -2px;
    right: -2px;
    background-color: #333333;
    border: 2px solid #666666;
    border-top: none;
    border-radius: 0 0 6px 6px;
    z-index: 10;

    ul {
      list-style-type: none;
      padding: 0;
      margin: 0;

      li {
        display: flex;
        align-items: center;
        padding: 4px;
        cursor: pointer;
        text-align: left;
        font-size: 16pt;

        &:hover {
          background-color: #444444;
        }

        img {
          width: auto;
          height: 80px;
          object-fit: cover;
          margin-right: 12px;
        }

        span {
          flex: 1;
        }
      }
    }
  }
}
</style>