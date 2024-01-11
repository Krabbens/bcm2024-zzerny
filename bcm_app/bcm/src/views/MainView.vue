<template>
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Rubik&display=swap" rel="stylesheet">
  </head>
  <ion-page>
    <ion-content :fullscreen="true" class="ion-padding" @click="show_map">
      <GoogleMap v-model="google_model" v-show="show_map_var" />
      <Searchbar v-model="value" @update:modelValue="updateSearchValueSolo($event)" @click.stop.prevent="show_searching" class="py-2 px-4"/>
      <div v-for="(searchbar, index) in searchbars" :key="index" class="flex py-2 px-4">
        <Searchbar v-model="searchbar.value" @update:modelValue="updateSearchValue(index, $event)" @click.stop.prevent="show_searching" v-show="dont_show_map_var" />
        <ion-button @click.stop.prevent="removeSearchBar" v-show="dont_show_map_var">+</ion-button>
      </div>
      <div class="flex justify-center space-x-8 py-4" v-show="dont_show_map_var">
        <ion-button @click.stop.prevent="addSearchBar" v-show="dont_show_map_var">+</ion-button>
        <ion-button @click.stop.prevent="showRoute" v-show="dont_show_map_var">Show route</ion-button>
      </div>
      <div class="flex justify-center space-x-8" v-show="show_map_var">
        <ion-button id="bolt_btn" style="--background: #38c223;" pill @click.prevent.stop="click_bolt">Bolt</ion-button>
        <ion-button id="mevo_btn" style="--background: rgb(180, 49, 49);" pill @click.prevent.stop="click_mevo">Mevo</ion-button>
        <ion-button id="tier_btn" style="--background: #5c319d;" pill @click.prevent.stop="click_tier">Tier</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent, IonButton } from '@ionic/vue';
import { FwbButton } from 'flowbite-vue';
import { getCurrentInstance, onMounted, ref } from 'vue';
import GoogleMap from '@/components/GoogleMap.vue';
import Searchbar from '@/components/Searchbar.vue';
import axios from 'axios';
const searchbars = ref([{ value: '' }]);
const zone_provider = ref('mevo');
const google_model = ref('');
const value = ref('');
const ret_route = ref([]);
const show_map_var = ref(true);
const dont_show_map_var = ref(false);

const mevo_button = ref(false);
const bolt_button = ref(false);
const tier_button = ref(false);

function click_mevo() {
  mevo_button.value = true;
  bolt_button.value = false;
  tier_button.value = false;

  if (mevo_button.value) {
    zone_provider.value = 'mevo';
  } else {
    zone_provider.value = '';
  }
  google_model.value = JSON.stringify(zone_provider.value);
}

function click_bolt() {
  bolt_button.value = true;
  mevo_button.value = false;
  tier_button.value = false;

  if (bolt_button.value) {
    zone_provider.value = 'bolt';
  } else {
    zone_provider.value = '';
  }
  google_model.value = JSON.stringify(zone_provider.value);
}

function click_tier() {
  tier_button.value = true;
  mevo_button.value = false;
  bolt_button.value = false;

  if (tier_button.value) {
    zone_provider.value = 'tier';
  } else {
    zone_provider.value = '';
  }
  google_model.value = JSON.stringify(zone_provider.value);
}

async function addSearchBar() {
  if (searchbars.value.length < 10)
  searchbars.value.splice(searchbars.value.length-1, 0, { value: '' });
  show_searching();
}

async function removeSearchBar(index) {
  if (searchbars.value.length > 1)
  searchbars.value.splice(index, 1);
  show_searching();
}

async function showRoute() {
  console.log('showRoute');
  show_map_var.value = true;
  dont_show_map_var.value = false;

  var addresses = [];
  addresses.push(value.value);
  searchbars.value.forEach((element) => {
    addresses.push(element.value);
  });
  
  const response = await axios.post(
    "https://classic-similarly-osprey.ngrok-free.app/bulkgeocodes",
    {
      addresses: addresses
    },
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });

  console.log(response);

  var iszone = true;
  if (zone_provider.value == 'mevo') {
    iszone = false;
  }

  const route = await axios.post(
    "https://classic-similarly-osprey.ngrok-free.app/getroute",
    { 
        "type": zone_provider.value,
        "point1" : {
            "lat" : response[0].lat,
            "lon" : response[0].lng
        },
        "point2" : {
            "lat" : response[1].lat,
            "lon" : response[1].lng
        },
        "zone" : iszone
    },
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });

  console.log(route);

  ret_route.value = [];
  ret_route.value.push(route.point1);
  for (var i = 1; i < response.length; i++) {
    ret_route.value.push(response[i]);
  }
  ret_route.value.push(route.point2);

  google_model.value = JSON.stringify(ret_route.value);
}

onMounted(() => {
  console.log('mounted');
  console.log(zone_provider);
});

async function show_map() {
  console.log('show_map');
  show_map_var.value = true;
  dont_show_map_var.value = false;
}

async function show_searching() {
  console.log('show_searching');
  show_map_var.value = false;
  dont_show_map_var.value = true;
}

function updateSearchValue(index, newValue) {
  searchbars.value[index].value = newValue;
  console.log(newValue);
}

function updateSearchValueSolo(newValue) {
  value.value = newValue;
  console.log(newValue);
}

</script>

<style scoped>
input {
  font-family: 'Rubik', sans-serif;
  font-weight: normal;
  font-size: large;
}

ion-content {
--background: none
}
</style>