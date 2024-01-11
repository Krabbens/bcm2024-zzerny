<template>
    <ion-list>
        <!-- Display existing inputs -->
        <ion-item v-for="(input, index) in inputs" :key="index">
        <ion-input v-model="inputs[index].value" :label="`Input ${index + 1}`"></ion-input>
        </ion-item>

        <!-- Button to add new input -->
        <ion-item>
        <ion-button @click="addInput">Add Input</ion-button>
        </ion-item>
    </ion-list>
  </template>
  
  <script>
  import { ref } from 'vue';

  
  export default {
    data() {
      return {
        inputs: [
          { value: '' }, // Initial input
          { value: '' }, // Initial input
        ],
      };
    },
    methods: {
      addInput() {
        this.inputs.push({ value: '' });
      },
    },
    components: {
      IonInput,
      IonItem,
      IonList,
    },
  };
  </script>
  
  <style scoped>
  
  </style>

