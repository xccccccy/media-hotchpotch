<template>
    <div class="mb-2 sm:mb-6 p-4 cursor-pointer" @click="$router.push('/book/' + book.book_id)">
        <div class="w-full sm:w-80 h-32">
            <div class=" w-24 h-32 float-left relative">
                <div class="book-shadow"></div>
                <img :src="book.img_url" :alt="book.name" loading="lazy" class="rounded w-full h-full" />
            </div>
            <div class="ml-28 text-left h-32">
                <div class=" font-semibold book-name hover:text-orange-500">{{ book.name }}</div>
                <div class=" text-tiny mt-1">作者：{{ book.author }}</div>
                <div class="resume text-tiny mt-3">{{ book.resume.replace(' ', '') }}</div>
            </div>
        </div>
        <div class="hidden h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500"
            :class="{ 'w-full': bottom_bar_hover, 'w-0': !bottom_bar_hover }"
            style="transition: width 0.1s ease-in-out 0s;">
        </div>
    </div>
</template>

<style></style>

<script setup>
import { ref, onUnmounted, watch, onMounted, reactive, computed } from 'vue'

defineProps(['book'])

</script>