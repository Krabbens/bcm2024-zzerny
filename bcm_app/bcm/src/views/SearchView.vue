<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Rubik&display=swap" rel="stylesheet">
    </head>
    <ion-page>
        <ion-content :fullscreen="true" class="ion-padding">
            <Searchbar @searchInput="handleSearchInput" />
            <Searchbar @searchInput="handleSearchInput" />
        </ion-content>
    </ion-page>
</template>

<script>
// Import the Searchbar component
import Searchbar from './Searchbar.vue';

export default {
    components: {
        Searchbar
    },
    data() {
        return {
            // Store search data from Searchbar components
            searchData: []
        };
    },
    methods: {
        // Handle search input event from Searchbar components
        handleSearchInput(data) {
            // Update the searchData array with the received data
            this.searchData.push(data);
            console.log(data)
        }
    }
};
</script>

