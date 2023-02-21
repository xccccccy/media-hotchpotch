<template>
  <div class="w-full bookinfo-back z-0">
    <div v-loading="!bookboxshow" class="bg-zinc-100 dark:bg-neutral-800 pb-8" style="min-height: 100vh;">
      <div class="bg-white dark:bg-zinc-800 pt-12 sm:pt-14">
        <div class="flex m-3 w-full sm:w-2/3 mx-auto pb-1 sm:pb-6 px-2">
          <img class="w-36 sm:w-56 rounded-md" style="aspect-ratio: 166/242;" :src="book.book_img_url"
            :alt="book.book_name" />
          <div class="bookinfo p-3 text-left pl-6 pb-0">
            <div class=" text-3xl"> {{ book.book_name }} </div>
            <div class="author">作者：{{ book.book_author }}</div>
            <div class="">更新：{{ book.book_last_update_time }}</div>
            <div class="hidden">连载</div>
            <div class="hidden sm:block">
              <div class="resume">{{ book.book_resume }}</div>
            </div>
            <div class="bookdo">
              <el-row>
                <el-button color="#626aef" plain size="large" auto-insert-space v-if="joinShelfBtnShow"
                  @click="joinbookshelf">加入书架</el-button>
                <el-button color="#626aef" plain size="large" auto-insert-space v-if="continueread_show"
                  @click="$router.push('/book/' + book.book_id + '/' + continueread_catalogue_id)">继续阅读</el-button>
              </el-row>
            </div>
          </div>
        </div>
        <div class="h-px bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500 w-full"></div>
      </div>
      <div class="w-full sm:w-2/3 mx-auto mt-3 sm:mt-8 bg-white dark:bg-zinc-800 shadow-2xl">
        <div class="block sm:block ">
          <h3 class="text-2xl font-bold mx-4 sm:mx-8 p-3 sm:pt-8 border-b border-black dark:border-white border-opacity-20 dark:border-opacity-20 text-left">作品简介</h3>
          <div class="resume mx-6 sm:mx-12 my-4 sm:my-10 text-lg">{{ book.book_resume }}</div>
        </div>
        <div class=" border-b border-black dark:border-white border-opacity-20 dark:border-opacity-20 mx-4 sm:mx-8 pb-3 pt-4 sm:pt-8 flex justify-between items-center">
          <h3 class="text-2xl font-bold px-3">
            <span>目录</span>
            <span class="directory-dot bg-black dark:bg-white"></span>
            <span>{{ book.catalogue_text_list.length }}章</span>
          </h3>
          <h3 class="px-4 text-xl font-medium cursor-pointer" @click="changeOrder">
            <span>{{ order ? "顺序" : "倒序" }}</span>
            <Reverse class="mx-1 inline-block text-sm"></Reverse>
          </h3>
        </div>
        <div class="book-catalogue-list m-5 sm:m-10 mb-0 mt-4 sm:mt-8">
          <cataloguebox v-for="(catalogue_text, index) in catalogue_text_list" key="index"
            :id="'catalogue_' + Number(order ? index + 1 : catalogue_text_list.length - index)" :catalogue_text="catalogue_text" :index="order ? index : catalogue_text_list.length - index - 1"
            :catalogue_href="book.catalogue_href_list[index]" :book_id="book.book_id"></cataloguebox>
        </div>
      </div>
    </div>
    <div class="catalogue_location">
      <a @click="tocontentid('#catalogue_' + continueread_catalogue_id)">
        <svg t="1648216386348" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="101090">
          <path
            d="M514.9184 931.7888a176.0256 176.0256 0 0 1-88.2688-23.6032c-159.3344-92.4672-279.5008-288.8704-279.5008-456.96 0-189.4912 150.3744-349.44 342.3232-364.1856 99.84-7.68 200.704 26.5728 276.6848 93.9008 74.3936 65.9456 117.6576 155.392 121.9072 251.904 7.936 182.016-106.2912 373.0432-284.3136 475.2896a178.5856 178.5856 0 0 1-88.832 23.6544z m2.3552-784.384c-7.68 0-15.36 0.3072-23.04 0.8704-160.1536 12.288-285.5936 145.3568-285.5936 302.9504 0 145.4592 109.312 322.816 248.8832 403.8144 35.3792 20.5312 79.6672 20.48 115.6096-0.1536 158.6176-91.136 260.5056-259.6352 253.5424-419.3792-3.4816-79.7184-39.424-153.8048-101.2736-208.5888-57.7024-51.2-132.5056-79.5136-208.128-79.5136z"
            fill="#333333" p-id="101091" />
          <path d="M517.7856 456.192m-132.096 0a132.096 132.096 0 1 0 264.192 0 132.096 132.096 0 1 0-264.192 0Z"
            fill="#F55C04" p-id="101092" />
        </svg>
      </a>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import { defineAsyncComponent } from 'vue'
import { getBookShelf, addBookToBookshelf } from './managebookshelf'
import { useHeaderStore } from '../../stores/header'
import Reverse from '~icons/carbon/arrows-vertical'

const cataloguebox = defineAsyncComponent(() => import('./cataloguebox.vue'))

export default {
  name: "bookinfo",
  data() {
    return {
      bookboxshow: false,
      book: {
        book_id: this.$route.params.book_id,
        book_name: "书籍名称",
        book_author: "某某某",
        book_state: "状态",
        book_last_update_time: "更新",
        book_last_catalogue_text: "最新",
        book_resume: "简介",
        book_img_url: "",
        catalogue_text_list: [],
        catalogue_href_list: [],
      },
      continueread_catalogue_id: 1,
      continueread_show: false,
      joinShelfBtnShow: true,
      order: true
    };
  },
  mounted() {
    this.initHeader();
    this.initCatalogue();
    this.initBookShelf();
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
          userSetting: {
            userLogHandle: this.userLog
          },
          homeSetting: {
            homeString: 'Home',
            homeHref: '/book'
          }
        }
      })
    },
    initCatalogue() {
      axios
        .get("/api/bookinfo/" + this.book.book_id)
        .then((res) => {
          this.bookboxshow = true;
          this.book = res.data;
          document.title = this.book.book_name;
        })
        .catch((err) => {
          ElNotification({ message: '请求失败！请刷新！', type: 'error', duration: 2000 });
          console.log(err);
        });
    },
    initBookShelf() {
      getBookShelf().then((res) => {
        if (res[this.book.book_id]) {
          this.continueread_show = true;
          this.joinShelfBtnShow = false;
          this.continueread_catalogue_id = res[this.book.book_id]["catalogue_id"];
        } else {
          this.continueread_show = false;
          this.joinShelfBtnShow = true;
        }
      })
    },
    joinbookshelf() {
      let book = {
        book_id: this.book.book_id,
        name: this.book.book_name,
        img_url: this.book.book_img_url,
        author: this.book.book_author,
        catalogue_id: 1,
        catalogue_name: this.book.catalogue_text_list[0],
      }
      addBookToBookshelf(book);
    },
    tocontentid(_selecter) {
      $("html,body").animate(
        {
          scrollTop: $(_selecter).offset().top - $(window).height() / 2,
        },
        70
      );
      $(_selecter).css({ background: "#000000b8" });
      $(_selecter + " a").css({ color: "#FFF" });
    },
    userLog(mode) {
      if (mode == 'login') {
        this.initBookShelf();
      }
    },
    changeOrder() {
      this.order = !this.order;
    }
  },
  computed: {
    catalogue_text_list() {
      return this.order ? this.book.catalogue_text_list : [...this.book.catalogue_text_list].reverse();
    }
  },
  components: {
    cataloguebox, Reverse
  },
};
</script>

<style scoped>
@import "../../assets/css/bookinfo.css";

.bookinfo {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.bookinfo-back::before {
  content: "";
  position: absolute;
  left: 0px;
  top: 0px;
  backdrop-filter: blur(45px) brightness(95%);
  height: 100%;
  width: 100%;
  z-index: -1;
}

.directory-dot {
  display: inline-block;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  margin: 0 10px;
  position: relative;
  top: -4px;
}
</style>
