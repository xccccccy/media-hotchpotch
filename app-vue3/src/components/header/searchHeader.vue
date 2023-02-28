<template>
    <div class="search hidden lg:flex w-1/2 xl:w-1/4 mx-4">
        <div class="muye-header-search bg-zinc-50 dark:bg-zinc-600">
            <input v-model="search_string" :placeholder="headerSetting.placeholder" @keyup.enter="headerSetting.clickHandle(search_string)">
            <Search class="search-icon text-zinc-900 dark:text-zinc-400" @click="headerSetting.clickHandle(search_string)"></Search>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import Search from '~icons/uil/search'

export default {
    name: "HomeHeader",
    components: { Search },
    props: {
        headerSetting: {
            type: Object
        }
    },
    setup() {

        const search_string = ref('')

        return { search_string };
    }
}

</script>

<style scoped>
.muye-header-search {
    display: inline-block;
    vertical-align: middle;
    position: relative;
    width: 100%;
    border-radius: 17px;
    padding: 5px 48px 7px 16px;
}

.muye-header-search input {
    border: 0;
    outline: 0;
    width: 100%;
    height: 100%;
    font-size: 14px;
    background: #fafafa00;
}

.muye-header-search .search-icon {
    font-size: 17px;
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
}

.search:hover {
    border-bottom: none !important;
}
</style>