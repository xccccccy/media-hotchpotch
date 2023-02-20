<template>
    <div class="flex w-full">
        <div class="flex-auto">
            <!-- player 一列 -->
            <div class="flex mb-4 items-center">
                <div @click="$emit('togglePanel')" class="flex items-center cursor-pointer pr-2">
                    <ArrowLeft class="h-4 px-2" />
                    <span> 返回 </span>
                </div>
                <el-divider direction="vertical" />
                <div class="pl-2">
                    <h3> {{ videoStore.playerOptions.name }}</h3>
                </div>
            </div>
            <div class="mb-3 mr-6 ml-1 sm:ml-0 shadow-xl relative" v-if="videoStore.playerOptions.iframeSrc == ''">
                <video-player :src="videoStore.playerOptions.src" :poster="videoStore.playerOptions.poster" controls
                    :loop="true" v-model:volume="videoStore.playerOptions.volume"
                    :muted="videoStore.playerOptions.muted" class="demo-player w-auto h-auto vjs-big-play-centered"
                    @mounted="handleMounted" @canplay="handleCanplay" @play="handlePlay"
                    @leavepictureinpicture="handleLeavepictureinpicture" />
                <div v-show="lastPlayshow && videoStore.lastPlay.currentTime > videoStore.playerOptions.currentTime"
                    @click="toLastPlay"
                    class=" absolute cursor-pointer px-2 py-1 text-sm bg-zinc-200 bg-opacity-80 text-zinc-800 rounded-md left-3 bottom-10">
                    跳转到上次观看位置: {{ lastPlayShowTime }}</div>
            </div>
            <div class="mb-3 mr-6 ml-1 sm:ml-0 shadow-xl relative" v-if="videoStore.playerOptions.iframeSrc != ''">
                <iframe class="demo-player w-full h-auto" :src="videoStore.playerOptions.iframeSrc" allow="fullscreen"></iframe>
            </div>
        </div>
        <div class="hidden sm:block" style="max-width: 21rem;min-width: 19rem;">
            <!-- 剧集列表 -->
            <div class="mt-10">
                <SeriesItem></SeriesItem>
            </div>
            <!-- 播放列表 -->
            <!-- <div class="">
                            <div class="my-2">播放列表</div>
                            <PlayList v-for="movie in videoList.slice(0, 10)" :key="movie.cover" :item="movie">
                            </PlayList>
                        </div> -->
        </div>
    </div>
    <div v-if="false">
        <div class="recommend-list">
            <RecommendedItem v-for="movie in recommendList" :key="movie.cover" :item="movie">
            </RecommendedItem>
        </div>
    </div>
</template>

<script setup>
import { ref, onUnmounted, watch, onMounted, reactive, computed } from 'vue'
import { VideoPlayer } from '@videojs-player/vue'
import 'video.js/dist/video-js.css'
import { ArrowLeft } from '@element-plus/icons-vue'

import { useVideoStore } from './videoStore'

import SeriesItem from './seriesItem.vue'
import RecommendedItem from './Recommended.vue'

import DATA from './data'
const recommendList = [DATA[2], DATA[4], DATA[1], DATA[0]]

const emit = defineEmits(['togglePanel'])

var videoStore = useVideoStore()

onMounted(() => {
    let newurl = location.href;
    if (newurl.indexOf('?') != -1) {
        let params = decodeURI(newurl.split("?")[1]);
        let s = params.split("=")[0];
        if (s == "p") {
            videoStore.showing = 'player'
            setTimeout(() => {
                document.getElementsByClassName('demo-player')[0].scrollIntoView({ block: "center" });
            }, 10)
        }
    }
    monitorkeydowm()
})

const monitorkeydowm = () => {
    document.onkeydown = (e) => {
        if (videoStore.showing != "player") {
            return;
        }
        let key = window.event.keyCode;
        if (key == 39 && videoStore.playerOptions.playing) {
            window.event.preventDefault()
            videoStore.player.currentTime(videoStore.lastPlay.currentTime + 5);
        } else if (key == 37 && !videoStore.playerOptions.playing) {
            window.event.preventDefault()
            videoStore.player.currentTime(videoStore.lastPlay.currentTime - 5);
        } else if (key == 38) {
            window.event.preventDefault()
            videoStore.playerOptions.volume += 0.05;
        } else if (key == 40) {
            window.event.preventDefault()
            videoStore.playerOptions.volume -= 0.05;
        } else if (key == 32) {
            window.event.preventDefault()
            if (videoStore.playerOptions.playing) {
                videoStore.pauseVideo()
            } else {
                videoStore.playVideo()
            }
        }
    };
}

const handleMounted = (payload) => {
    videoStore.player = payload.player;
    videoStore.playerOptions.currentTime = computed(() => {
        if (videoStore.lastPlay.currentTime < payload.state.currentTime) {
            videoStore.lastPlay.currentTime = payload.state.currentTime;
        }
        return payload.state.currentTime;
    });
    videoStore.playerOptions.duration = computed(() => {
        return payload.state.duration;
    });
    videoStore.playerOptions.playing = computed(() => {
        return payload.state.playing;
    })
    videoStore.playerOptions.isFullscreen = computed(() => {
        return payload.state.isFullscreen;
    })
    videoStore.playerOptions.isPip = computed(() => {
        return payload.state.isInPictureInPicture;
    })
}

const handleCanplay = () => {
    console.log("Player can play.")
}

const lastPlayshow = ref(false)

let lastPlayshowed = false;
const handlePlay = () => {
    if (lastPlayshowed) {
        return;
    }
    lastPlayshowed = true;
    if (videoStore.videoItem.id == videoStore.lastPlay.id) {
        lastPlayshow.value = true;
        setTimeout(() => {
            if (videoStore.lastPlay.currentTime >= videoStore.playerOptions.currentTime) {
                videoStore.lastPlay.currentTime = videoStore.playerOptions.currentTime;
            }
            lastPlayshow.value = false;
        }, 12000);
    } else {
        videoStore.lastPlay = {
            id: videoStore.videoItem.id,
            currentTime: 0,
            duration: 0,
            seeked: false
        }
    }
}

const handleLeavepictureinpicture = (e) => {
    console.log("handleLeavepictureinpicture", e);
    if (videoStore.showing != "player") {
        videoStore.pauseVideo();
    }
}

const toLastPlay = () => {
    videoStore.player.currentTime(videoStore.lastPlay.currentTime);
}

const lastPlayShowTime = computed(() => {
    return secTotime(videoStore.lastPlay.currentTime)
})

const secTotime = (s) => {
    var t = '';
    if (s > -1) {
        var hour = Math.floor(s / 3600)
        var min = Math.floor(s / 60) % 60
        var sec = s % 60
        if (hour > 0) {
            if (hour < 10) {
                t = '0' + hour + ":"
            } else {
                t = hour + ":"
            }
        }
        if (min < 10) {
            t += "0"
        }
        t += min + ":"
        if (sec < 10) {
            t += "0"
        }
        t += sec.toFixed(0)
    }
    return t
}

</script>

<style scoped>
.demo-player {
    aspect-ratio: 5 / 3;
}
</style>