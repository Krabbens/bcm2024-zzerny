<template>
    <fwb-input v-model="searchValue" placeholder="enter your search query" class="w-3/4">
        <template #prefix>
            <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor"
                viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round"
                    stroke-width="2" />
            </svg>
        </template>
    </fwb-input>
</template>

<script setup>
import { ref, watch } from 'vue';
import { FwbInput } from 'flowbite-vue';

const searchValue = ref('');

watch(() => searchValue, (newValue) => {
  // Emit an event to notify the parent component about the value change
  emit('update:modelValue', newValue);
});

</script>