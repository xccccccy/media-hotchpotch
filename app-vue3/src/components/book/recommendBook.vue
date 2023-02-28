<template>
    <div>
        <!-- 上面 hot_book | top_book -->
        <div class="flex">
            <div class=" w-2/3">
                <h3
                    class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                    <span class="pl-4">主编力荐</span>
                </h3>
                <div class="flex flex-wrap  justify-around">
                    <SearchBook v-for="book in recommendBooks.hot_book" :key="book.book_id" :book="book"></SearchBook>
                </div>
            </div>
            <div class=" w-1/4 ml-8">
                <h3
                    class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                    <span class="pl-3">强力推荐</span>
                </h3>
                <div class="flex flex-col items-start">
                    <div v-for="book in recommendBooks.top_book" class=" cursor-pointer px-2 pt-3 flex w-full items-end"
                        @click="$router.push('/book/' + book.book_id)">
                        <span class="px-2 text-tiny text-zinc-700 dark:text-zinc-300">[{{ book.type }}]</span>
                        <span class="">{{ book.name }}</span>
                        <span class="text-tiny ml-auto">{{ book.author }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <!-- 下面 type_book -->
            <div>
                <div v-for="(type_books, type) in recommendBooks.type_book">
                    <h3
                        class="m-2 py-3 text-left text-xl font-medium border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                        <span class="pl-3"> {{ type }} </span>
                    </h3>
                    <div>
                        <div>
                            <div>
                                <span>1</span>
                                <img :src="type_books.block_top_book.img_url">
                                <span>{{ type_books.block_top_book.name }}</span>
                                <span class="">{{ type_books.block_top_book.name }}</span>
                            </div>
                        </div>
                        <div>
                            <div v-for="(book, index) in type_books.block_other_books"
                                class=" cursor-pointer px-2 pt-3 flex w-full items-end"
                                @click="$router.push('/book/' + book.book_id)">
                                <span>{{ index + 2 }}</span>
                                <span class="px-2 text-tiny text-zinc-700 dark:text-zinc-300">[{{ book.type }}]</span>
                                <span class="">{{ book.name }}</span>
                                <span class="text-tiny ml-auto">{{ book.author }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style></style>

<script setup>
import { ref, onUnmounted, watch, onMounted, reactive, computed } from 'vue'
import axios from 'axios';

import SearchBook from './searchbookbox.vue';

defineProps(['book'])

const recommendBooks = ref({ hot_book: [{ author: "青鸾峰上", book_id: "99568", img_url: "https://www.quge3.com/bookimg/99779.jpg", name: "我有一剑", resume: "我有一剑，出鞘即无敌！......" }], top_book: [], type_book: {} })

onMounted(() => {
    axios.post('/api/book/recommend').then((res) => {
        console.log(res.data)
        recommendBooks.value = res.data.data;
        console.log(recommendBooks)
    })
})

</script>