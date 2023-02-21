<template>
  <div class="cataloguebox p-3 w-full sm:w-1/3 border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 sm:border-none">
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
