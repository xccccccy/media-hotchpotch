<template>
  <div class="cataloguebox px-1 py-3 sm:p-3 w-full sm:w-1/3 border-b sm:border-none border-black dark:border-white border-opacity-5 dark:border-opacity-5">
    <div class="catalogue">
      <a @click="$router.push('/book/' + book_id + '/' + String(index + 1))">{{ catalogue_text }}</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "cataloguebox",
  props: ["catalogue_text", "index", "catalogue_href", "book_id"],
  methods: {
    select_book(book_id) {
      console.log(book_id);
    },
  },
};
</script>

<style scoped>
.cataloguebox {
  text-align: left;
}

.cataloguebox a {
  text-decoration: none;
  cursor: pointer;
}
</style>
