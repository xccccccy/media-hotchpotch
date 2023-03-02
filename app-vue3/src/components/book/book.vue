<template>
    <div class="w-full sm:w-3/4 2xl:w-2/3 pt-16 lg:pt-20">
        <div class="my-1 px-1 block lg:hidden">
            <div class="muye-header-search bg-zinc-200 dark:bg-zinc-600">
                <input v-model="search_string" placeholder="搜索书籍" @keyup.enter="searchbook()">
                <Search class="search-icon text-zinc-900 dark:text-zinc-400" @click="searchbook()"></Search>
            </div>
        </div>
        <div class="p-1 pb-8">
            <div v-if="type_show == 'home'">
                <RecommendBook></RecommendBook>
            </div>
            <div v-if="type_show == 'bookshelf'">
                <div class="text-left text-xl font-medium p-2 ml-1 mb-2 border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 ">
                    <span>我的书架</span>
                </div>
                <div class="flex flex-wrap justify-between">
                    <Bookshelfbox v-for="book in bookshelf" :key="book.book_id" :book="book" @delBook="delbook">
                    </Bookshelfbox>
                </div>
            </div>
            <div v-if="type_show == 'search'">
                <div class="text-left text-xl font-medium p-2 ml-1 mb-2 border-b border-black dark:border-white border-opacity-10 dark:border-opacity-10 " v-show="search_info.length != 0">
                    <span class="pl-1" v-html="search_info"></span>
                </div>
                <div class="flex flex-wrap justify-between" v-loading="searchloading">
                    <SearchBookbox v-for="book in search_books" :key="book.book_id" :book="book"></SearchBookbox>
                </div>
            </div>
            <div class="shang-list" v-if="type_show == 'shang'">
                <div class="shang flex-col xl:flex-row">
                    <div>
                        <img src="@/assets/img/wx_shou.jpg" loading="lazy" class="shadow-2xl" />
                    </div>
                    <div>
                        <img src="@/assets/img/zfb_shou.jpg" loading="lazy" class="shadow-2xl" />
                    </div>
                    <div>
                        <img src="@/assets/img/wx_zan.jpg" loading="lazy" class="shadow-2xl" />
                    </div>
                </div>
            </div>
        </div>
        <!-- <Like></Like> -->
    </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import { defineAsyncComponent, markRaw } from 'vue'
import Search from '~icons/uil/search'
import { getBookShelf, fromBookshelfDelBook, addBookToBookshelf } from './managebookshelf'
import Like from "../like.vue";
import { useHeaderStore } from '../../stores/header'
import CarbonBook from '~icons/carbon/book'
import CarbonSearch from '~icons/carbon/search'
import notoMoneyBag from '~icons/healthicons/money-bag-outline'
import RecommendBook from './recommendBook.vue'

const SearchBookbox = defineAsyncComponent(() => import('./searchbookbox.vue'))
const Bookshelfbox = defineAsyncComponent(() => import('./bookshelfbox.vue'))

export default {
    name: "book",
    data() {
        return {
            search_string: '',
            type_show: 'home',
            search_data: null,
            search_books: null,
            search_info: "暂无搜索...",
            bookshelf: null,
            searchloading: false,
            ismobile: false,
        };
    },
    watch: {
    },
    computed: {
    },
    mounted() {
        this.initHeader();
        this.initLocalStorage();
        this.initSearchUrl();
        this.initBookShelf();
        this.judgeismobile();
        document.title = "My Book";
        $("html,body").scrollTop(0);
    },
    unmounted() {
        const headerStore = useHeaderStore()
        headerStore.resetHeader()
    },
    methods: {
        initHeader() {
            const headerStore = useHeaderStore()
            headerStore.$patch({
                headerSetting: {
                    headerSettings:
                        [
                            {
                                type: 'search',
                                placeholder: "搜索书籍",
                                clickHandle: this.searchbook,
                                position: "right"
                            },
                            // {
                            //     type: 'common',
                            //     // headerString: '搜索',
                            //     iconSetting: markRaw(CarbonSearch),
                            //     clickHandle: this.back_search
                            // },
                            {
                                type: 'common',
                                headerString: '首页',
                                // iconSetting: markRaw(CarbonBook),
                                clickHandle: () => {this.type_show = 'home'}
                            },
                            {
                                type: 'common',
                                headerString: '书架',
                                // iconSetting: markRaw(CarbonBook),
                                clickHandle: this.backbookshelf
                            },
                            {
                                type: 'common',
                                headerString: 'Shǎng',
                                // iconSetting: markRaw(notoMoneyBag),
                                clickHandle: this.shangqian,
                                style: "color: #CD9D02"
                            }
                        ],
                    userSetting: {
                        userLogHandle: this.userLog
                    }
                }
            })
        },
        initBookShelf() {
            this.bookshelf = JSON.parse(localStorage.bookshelf);
            getBookShelf().then((res) => {
                this.bookshelf = res;
            });
        },
        searchbook(s) {
            let search_s = s || this.search_string;
            this.search_string = search_s;
            this.searchloading = true;
            this.search_info = "正在搜索中...";
            this.type_show = 'search';
            this.$router.push("/book?s=" + search_s);
            axios
                .post("/api/book/search", {
                    search_string: search_s,
                })
                .then((res) => {
                    this.searchloading = false;
                    (document.title = "'" + search_s + "'" + "_搜索"),
                        (this.search_books = res.data.data);
                    if (this.search_books.length) {
                        this.search_info = '搜索结果：';
                    } else {
                        this.search_info =
                            '😭 暂未找到与"<b>' + search_s + '</b>"相关的书籍';
                    }
                })
                .catch((err) => {
                    this.searchloading = true;
                    ElNotification({ message: '请求失败！请刷新！', type: 'error', duration: 0 });
                    console.log(err);
                });
        },
        backbookshelf() {
            this.type_show = 'bookshelf';
        },
        back_search() {
            this.type_show = 'search';
        },
        shangqian() {
            this.type_show = 'shang';
        },
        delbook(book_id) {
            this.bookshelf = fromBookshelfDelBook(book_id);
        },
        judgeismobile() {
            var ua = navigator.userAgent;
            var ipad = ua.match(/(iPad).*OS\s([\d_]+)/),
                isIphone = !ipad && ua.match(/(iPhone\sOS)\s([\d_]+)/),
                isAndroid = ua.match(/(Android)\s+([\d.]+)/),
                isMobile = isIphone || isAndroid;
            //判断
            if (isMobile) {
                this.ismobile = true;
            }
        },
        initSearchUrl() {
            let newurl = location.href;
            if (newurl.indexOf('?') != -1) {
                let s = decodeURI(newurl.split("=")[1]);
                this.searchbook(s);
            }
        },
        initLocalStorage() {
            let LSversion = '1.02'
            if (!localStorage.LSversion || localStorage.LSversion != LSversion) {
                localStorage.clear();
                localStorage.LSversion = LSversion;
            } else {
                return
            }
            if (!localStorage.bookshelf) {
                localStorage.bookshelf = "{}";
            }
            let InfiniteReadaheadSet = { "preContentShow": true, "nextContentShowed": false, "isSwitched": false, "nowContentSelecter": "now", "ifShouldLoadNext": false };
            if (!localStorage.InfiniteReadaheadSet) {
                localStorage.InfiniteReadaheadSet = JSON.stringify(InfiniteReadaheadSet);
            }
            let setting = {
                'currentFontsize': 1.4,
                'light': {
                    'currentbjcolor': "linear-gradient(to right, #322e30, #3b363e, #3e414e, #3b4d5d, #335a66, #37666f, #3d7376, #467f7b)",
                    'currentskin': ["#000", "rgba(255,255,255,0.7)"]
                },
                'dark': {
                    'currentbjcolor': "linear-gradient(to right, #322e30, #3b363e, #3e414e, #3b4d5d, #335a66, #37666f, #3d7376, #467f7b)",
                    'currentskin': ["#000", "rgba(255,255,255,0.7)"]
                },
                'currentlineheight': 1.8,
                'Infinitereadahead': false,
                'readahead': true,
            }
            if (!localStorage.setting) {
                localStorage.setting = JSON.stringify(setting);
            }
            if (!localStorage.darkmode) {
                localStorage.darkmode = 'auto';
            }
        },
        userLog(mode) {
            if (mode == 'login') {
                getBookShelf().then((res) => {
                    this.bookshelf = res;
                    this.type_show = 'bookshelf';
                });
            } else {
                getBookShelf().then((res) => {
                    this.bookshelf = res;
                });
            }
        },
        test() {
        },
    },
    components: {
        SearchBookbox: SearchBookbox,
        Bookshelfbox: Bookshelfbox,
        Search: Search,
        Like,
        RecommendBook
    }
};
</script>

<style scoped>
@import "../../assets/css/book.css";

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
</style>
