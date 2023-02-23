<template>
  <div @mouseenter="bottom_bar_hover = true" @mouseleave="bottom_bar_hover = false" class="mb-2 sm:mb-6 p-4 cursor-pointer" @click="$router.push('/book/' + book.book_id)">
    <div class="w-full sm:w-80 h-32">
      <div class=" w-24 h-32 float-left relative" @click="$router.push('/book/' + book.book_id)">
        <div class="book-shadow"></div>
        <img :src="book.img_url" :alt="book.name" loading="lazy" class="rounded w-full h-full"/>
      </div>
      <div class="ml-28 text-left h-32">
        <div class=" font-semibold book-name hover:text-orange-500">{{ book.name }}</div>
        <div class=" text-tiny mt-1">作者：{{ book.author }}</div>
        <div class="resume text-tiny mt-3">{{ book.resume.replace(' ', '') }}</div>
      </div>
    </div>
    <div class="hidden h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500"
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
.book-shadow {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background: url(data:image/png;base64,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) no-repeat 50%;
  background-size: 100% 100%;
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
