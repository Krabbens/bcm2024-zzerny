<template>
  <div class="container" style="position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;">
    <capacitor-google-map
      ref="mapRef"
      style="position:absolute; width: 100vw; height: 100vh;"
    >
    </capacitor-google-map>
  </div>
</template>

<script setup lang="ts">
const model = defineModel()
import { GoogleMap, Polygon, Marker, Polyline} from '@capacitor/google-maps';
import { decode, encode } from "@googlemaps/polyline-codec";
import { environment } from '../environments/environment';
import { onMounted, watch } from 'vue';
import { ref, nextTick } from 'vue';
import { IonAccordion, IonAccordionGroup, IonItem, IonLabel } from '@ionic/vue';
import { defineComponent } from 'vue';
import { useToast, POSITION } from "vue-toastification";
import axios from 'axios';
import Vue from 'vue';



const mapRef = ref<HTMLElement>();
let newMap: GoogleMap;
const toast = useToast();
const counter: any = [];
const markers: any = [];
const route = ref([]);

const palette: any = {
  "no-go": "#FFADAD",
  "reduced-speed": "#FDFFB6",
  "parking": "#D9EDF8",
  "parking-mode": "#DEDAF4",
  "no-parking": "#FFD6A5",
}

const palette_opacity: any = {
  "no-go": 0.8,
  "reduced-speed": 0.7,
  "parking": 0.9,
  "parking-mode": 0.9,
  "no-parking": 0.7,
}

const type_of_vehicle: any = {
  "bolt": "https://cdn.discordapp.com/attachments/1194605213978472558/1194896204648165376/scooter.svg?ex=65b204cf&is=659f8fcf&hm=0241dba70428310291acd9701075009c7541cc9f609dc63eb21ce192c18b339a&",
  "tier": "https://cdn.discordapp.com/attachments/1194605213978472558/1194896204648165376/scooter.svg?ex=65b204cf&is=659f8fcf&hm=0241dba70428310291acd9701075009c7541cc9f609dc63eb21ce192c18b339a&",
  "mevo": "https://cdn.discordapp.com/attachments/1194605213978472558/1194897053810163712/bike.svg?ex=65b20599&is=659f9099&hm=21a6f7a02f9a263fd9ec50e8acf4bacb9a49be7ffdfe49afbdf9c719f6f6e84f&"
}

onMounted(async () => {
  await nextTick();
  await createMap();
  await addMarker();
  await addPolygons();
});

watch(model, async (newValue) => {
  try {
    await deleteAllMarkers();
    await deleteAllPolygons();
    await addPolygons();
    await addMarker();
  }
  catch (error) {
    console.log(error);
    location.reload();
  }
});

async function createMap() {
  newMap = await GoogleMap.create({
    id: "my-cool-map",
    element: mapRef.value,
    apiKey: environment.keys.googleMaps,
    config: {
      center: {
        lat: 54.372158,
        lng: 18.638306,
      },
      zoom: 12,
    },
  });
}

async function addMarker() {
  if (JSON.parse(model.value) != "bolt" && JSON.parse(model.value) != "tier" && JSON.parse(model.value) != "mevo") {
    return;
  }
  const response = await axios.get("https://classic-similarly-osprey.ngrok-free.app/getvehicles/" + JSON.parse(model.value), 
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });
  await response.forEach((element: any) => {
    const marker = [{
      coordinate: element.location,
      title: element.name,
      snippet: element.type,
      iconUrl: type_of_vehicle[element.brand],
    }] as Marker[];
    newMap.addMarkers(
      marker
    ).then((retval) => {
      markers.push(retval[0]);
    });
  });
}

async function addPolygons() {
  if (JSON.parse(model.value) != "bolt" && JSON.parse(model.value) != "tier") {
    return;
  }
  console.log("addPolygons");
  const response = await axios.get("https://classic-similarly-osprey.ngrok-free.app/getzones/" + JSON.parse(model.value), 
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });
  await response.forEach((element: any) => {
    const pol = [{
      paths: element.coordinates,
      strokeColor: "#FF0000",
      strokeOpacity: 0.9,
      strokeWeight: 0.05,
      fillColor: palette[element.type],
      fillOpacity: 0.4,
    }] as Polygon[];
    const retval = newMap.addPolygons(
      pol
    ).then((retval) => {
      counter.push(retval[0]);
    });
    console.log(retval)
  });
}

async function deleteAllPolygons() {
  console.log(counter)
  newMap.removePolygons(counter);
}

async function deleteAllMarkers() {
  console.log(markers)
  newMap.removeMarkers(markers);
}

async function getCoordinates(event: any) {
    console.log(event.clientX);

    console.log(event.clientY);
}

async function getRoutes() {
  if (JSON.parse(model.value) == "bolt" || JSON.parse(model.value) == "tier" || JSON.parse(model.value) == "mevo") {
    return;
  }

  var routes = JSON.parse(model.value);
  console.log('getRoutes');
  const response = await axios.post(
    "https://classic-similarly-osprey.ngrok-free.app/wholeroute",
    { 
        adresses: routes
    },
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });
  
async function addPolylines() {
  if (JSON.parse(model.value) == "bolt" || JSON.parse(model.value) == "tier" || JSON.parse(model.value) == "mevo") {
    return;
  }
  console.log("addPolygons");
  const response = await axios.post("https://classic-similarly-osprey.ngrok-free.app/wholeroute",
    {
      adresses: routes
    }, 
    {
      headers: {
        'ngrok-skip-browser-warning': 'true'
      }
    }
  ).then((response) => {
    return response.data;
  });
  await response.forEach((element: any) => {
    const pol = [{
      tag: element,
    }] as Polyline[];
    const retval = newMap.addPolylines(
      pol
    ).then((retval) => {
      counter.push(retval[0]);
    });
    console.log(retval)
  });
}


  
}
</script>





<style scoped>
capacitor-google-map {
display: inline-block;
height: 100%;
width: 100%;
}

ion-content {
--background: none
}
</style>
