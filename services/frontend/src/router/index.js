import {createRouter, createWebHistory} from 'vue-router'
import SearchView from '@/views/SearchView.vue'
import EpisodesView from "@/views/EpisodesView";
import ContentSearchView from "@/views/ContentSearchView";
import ContentResultsView from "@/views/ContentResultsView";

const routes = [
    {
        path: '/',
        name: 'search',
        component: SearchView
    },
    {
        path: '/episodes',
        name: 'episodes',
        component: EpisodesView
    },
    {
        path: '/episode',
        name: 'episode',
        component: ContentSearchView
    },
    {
        path: '/content_results',
        name: 'content_results',
        component: ContentResultsView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
