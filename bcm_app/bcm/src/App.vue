<template>
  <head>
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"> 
  </head>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
</script>
