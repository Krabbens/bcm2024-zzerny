import { defineCustomElements } from '@ionic/pwa-elements/loader';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import Toast, { PluginOptions } from "vue-toastification";
import "vue-toastification/dist/index.css";

import { IonicVue } from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

const options: PluginOptions = {
  // You can set your default options here
};

/* Theme variables */
import './theme/variables.css';
defineCustomElements(window);
const app = createApp(App)
  .use(IonicVue)
  .use(router)
  .use(Toast, options);


  
router.isReady().then(() => {
  app.mount('#app');
});