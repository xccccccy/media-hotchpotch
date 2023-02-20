<template>
    <div class="">
        <div class="app w-24/25 lg:w-10/12 xl:w-9/12 pt-3 text-left pb-14 mx-auto">
            <div class="main">
                <div v-show="videoStore.showing == 'search'">
                    <SearchRelation @togglePanel="togglePanel" ref="searchComponent"></SearchRelation>
                </div>
                <div v-show="videoStore.showing == 'info'">
                    <VideoInfo></VideoInfo>
                </div>
                <div v-show="videoStore.showing == 'player'">
                    <PlayerRelation @togglePanel="togglePanel"></PlayerRelation>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onUnmounted, watch, onMounted, reactive, computed } from 'vue'
import { useHeaderStore } from '../../stores/header'

import SearchRelation from './searchRelation.vue'
import VideoInfo from './videoInfo.vue'
import PlayerRelation from './playerRelation.vue'

import { useVideoStore } from './videoStore'

const searchComponent = ref(null)
var videoStore = useVideoStore()

const togglePanel = () => {
    // if (!videoStore.playerOptions.isPip) {
    //     videoStore.pauseVideo();
    // }
    if (videoStore.showing == 'search') {
        videoStore.showing = 'player'
        setTimeout(() => {
            document.getElementsByClassName('demo-player')[0].scrollIntoView({ block: "center" });
        }, 10)
    } else {
        videoStore.showing = 'search'
        videoStore.player.requestPictureInPicture();
    }
}


const searchVideo = (s) => {
    searchComponent.value.searchVideo(s);
}

const headerStore = useHeaderStore();
headerStore.$patch({
    headerSetting: {
        headerSettings: [
            {
                type: 'search',
                placeholder: "搜索",
                clickHandle: searchVideo
            }
        ]
    }
})

onUnmounted(() => {
    headerStore.resetHeader();
    document.onkeydown = null;
})
</script>
  
<style scoped>
.main>div {
    min-height: 80vh;
    width: 100%;
}
</style>