<template>
  <div class="mb-2 sm:mb-6 p-4">
    <div class="w-full sm:w-80 h-40 sm:h-32 relative">
      <div class="w-32 sm:w-24 h-40 sm:h-32 float-left relative cursor-pointer"
        @click="$router.push('/book/' + book.book_id)">
        <div class="book-shadow"></div>
        <img :src="book.img_url" :alt="book.name" loading="lazy" class="rounded w-full h-full" />
      </div>
      <div class="ml-36 sm:ml-28 text-left h-40 sm:h-32">
        <div class="cursor-pointer font-semibold book-name hover:text-orange-500 text-lg sm:text-base"
          @click="$router.push('/book/' + book.book_id)">{{
            book.name }}</div>
        <div class="text-base sm:text-tiny mt-6 sm:mt-3">作者：{{ book.author }}</div>
        <div class="text-base sm:text-tiny mt-2 sm:mt-1 max-one">上次读到：{{ book.catalogue_name }}</div>
        <div class="mt-4 sm:mt-3 flex">
          <button class="mybtn min-w-fit"
            @click="$router.push('/book/' + book.book_id + '/' + book.catalogue_id)">继续阅读</button>
          <button class="mybtn min-w-fit" @click="$router.push('/book/' + book.book_id)">查看目录</button>
        </div>
      </div>
      <div @click="$emit('delBook', book.book_id)" class="del absolute right-0 top-0">
        <svg viewBox="0 0 1024 1024" class="dark:fill-white hover:fill-red-700">
          <path
            d="M548.2496 512L857.7024 202.3424a25.6 25.6 0 1 0-36.2496-36.2496L512 475.7504 202.3424 166.2976a25.6 25.6 0 0 0-36.0448 36.0448L475.7504 512 166.2976 821.6576a25.6 25.6 0 1 0 36.2496 36.2496L512 548.2496l309.6576 309.4528a25.6 25.6 0 0 0 36.2496-36.2496z"
            p-id="72105" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "bookshelfbox",
  data() {
    return {

    }
  },
  props: ["book"],
  emits: ["delBook"],
  methods: {
    select_book(book_id) {
      console.log(book_id);
    },
  },
};
</script>

<style scoped>
.del {
  line-height: 0;
  cursor: pointer;
}

.del svg {
  height: 1.3rem;
  float: right;
}

.el-button {
  background-color: rgba(202, 202, 202, 1);
}

.el-button:hover {
  background-color: #626aef;
}

.max-one {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  text-overflow: -o-ellipsis-lastline;
  text-overflow: ellipsis;
  word-break: break-word;
  -webkit-line-clamp: 1;
}
</style>
