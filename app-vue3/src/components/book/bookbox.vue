<template>
  <div @mouseenter="bottom_bar_hover = true" @mouseleave="bottom_bar_hover = false" @click="$router.push('/book/' + book.book_id)">
    <div>
      <img :src="book.img_url" :alt="book.name" loading="lazy" />
      <div>
        <div class="">{{ book.name }}</div>
        <div class="">作者：{{ book.author }}</div>
        <div class="resume">{{ book.resume }}</div>
      </div>
    </div>
    <div class="h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500"
      :class="{ 'w-full': bottom_bar_hover, 'w-0': !bottom_bar_hover }" style="transition: width 0.1s ease-in-out 0s;">
    </div>
  </div>
</template>

<script>
export default {
  name: "bookbox",
  props: ["book"],
  data() {
    return {
      bottom_bar_hover: false,
    }
  },
  methods: {
    select_book(book_id) {
      console.log(book_id);
    },
  },
};
</script>

<style scoped>
.resume {
  line-height: 1.7;
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  text-overflow: -o-ellipsis-lastline;
  text-overflow: ellipsis;
  word-break: break-word;
  -webkit-line-clamp: 2;
}
</style>
