<template>
    <div v-loading.fullscreen.lock="fullscreenLoading">
        <!-- 上面 hot_book | top_book -->
        <div class="flex">
            <div class="w-full sm:w-2/3">
                <h3
                    class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                    <span class="pl-4">热榜推荐</span>
                </h3>
                <div class="flex flex-wrap  justify-around">
                    <SearchBook v-for="book in recommendBooks.hot_book" :key="book.book_id" :book="book"></SearchBook>
                </div>
            </div>
            <div class=" w-1/4 ml-8 hidden sm:block">
                <h3
                    class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                    <span class="pl-3">强力推荐</span>
                </h3>
                <div class="flex flex-col items-start">
                    <div v-for="book in recommendBooks.top_book"
                        class=" cursor-pointer px-2 pt-3 flex w-full items-end whitespace-nowrap"
                        @click="$router.push('/book/' + book.book_id)">
                        <span class="px-2 text-tiny text-zinc-700 dark:text-zinc-300">[{{ book.type }}]</span>
                        <span class="text-warp hover:text-orange-500">{{ book.name }}</span>
                        <span class="text-warp text-tiny ml-auto">{{ book.author }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <!-- 下面 type_book -->
            <div class="flex flex-wrap">
                <div v-for="(type_books, type) in recommendBooks.type_book" class="w-full sm:w-1/3 p-4">
                    <h3
                        class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                        <span class="pl-3"> {{ type }} </span>
                    </h3>
                    <div>
                        <div>
                            <div class=" w-24 h-32 float-left relative mx-3 cursor-pointer"
                                @click="$router.push('/book/' + type_books.block_top_book.book_id)">
                                <div class="book-shadow"></div>
                                <img :src="type_books.block_top_book.img_url" :alt="type_books.block_top_book.name"
                                    loading="lazy" class="rounded w-full h-full" />
                            </div>
                            <div class="flex flex-col text-left">
                                <span class="font-semibold book-name hover:text-orange-500 mt-1 cursor-pointer"
                                    @click="$router.push('/book/' + type_books.block_top_book.book_id)">
                                    {{ type_books.block_top_book.name }}</span>
                                <span class="resume text-tiny mt-5 text-zinc-700 dark:text-zinc-200">
                                    {{ type_books.block_top_book.resume }}</span>
                            </div>
                        </div>
                        <div>
                            <div v-for="(book, index) in type_books.block_other_books"
                                class=" cursor-pointer px-2 pt-3 flex w-full items-end whitespace-nowrap"
                                @click="$router.push('/book/' + book.book_id)">
                                <span class="px-2 text-tiny text-zinc-700 dark:text-zinc-300">[{{ book.type }}]</span>
                                <span class="text-warp hover:text-orange-500">{{ book.name }}</span>
                                <span class="text-warp text-tiny ml-auto">{{ book.author }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.book-shadow {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background: url(data:image/png;base64,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) no-repeat 50%;
    background-size: 100% 100%;
}

.text-warp {
    overflow: hidden;
    text-overflow: ellipsis;
}

.book-name {
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: -o-ellipsis-lastline;
    text-overflow: ellipsis;
    word-break: break-word;
    -webkit-line-clamp: 1;
}

.resume {
    line-height: 1.5;
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: -o-ellipsis-lastline;
    text-overflow: ellipsis;
    word-break: break-word;
    -webkit-line-clamp: 3;
}
</style>

<script setup>
import { ref, onUnmounted, watch, onMounted, reactive, computed } from 'vue'
import axios from 'axios';

import SearchBook from './searchbookbox.vue';

const fullscreenLoading = ref(true)

const recommendBooks = ref({
    hot_book: [
        { author: "加载中...", book_id: "99568", img_url: "", name: "加载中...", resume: "加载中..." },
        { author: "加载中...", book_id: "99568", img_url: "", name: "加载中...", resume: "加载中..." },
        { author: "加载中...", book_id: "99568", img_url: "", name: "加载中...", resume: "加载中..." },
        { author: "加载中...", book_id: "99568", img_url: "", name: "加载中...", resume: "加载中..." }],
    top_book: [], type_book: {}
})

onMounted(() => {
    axios.post('/api/book/recommend').then((res) => {
        fullscreenLoading.value = false;
        recommendBooks.value = res.data.data;
    })
})

</script>