<template>
    <div
        class="movie-item border rounded-md shadow-xl bg-violet-50 dark:bg-slate-700 dark:bg-opacity-80  dark:border-opacity-20 dark:border-violet-500">
        <div class="cover cursor-pointer" @click="changeVideo(0)">
            <img :src="item.pic" alt="cover" loading="lazy" />
            <div class="duration">{{ item.note }}</div>
        </div>
        <div class="detail flex-1 py-4 px-5 flex flex-col relative" style="">
            <!-- <img :src="sourceLogo"  /> -->
            <!-- <iqiyilogo></iqiyilogo>
            <qqlogo class=" hidden"></qqlogo> class=" opacity-60 w-1/5 absolute right-6"-->
            <div class="title cursor-pointer flex w-full items-baseline" @click="changeVideo(0)">
                <div class="mx-1 text-tiny font-normal bg-blue-100 dark:bg-slate-500 rounded" style="padding: 2px 6px;">
                    {{ item.type }}
                </div>
                <span>{{ item.name }}</span>
                <div class="mx-1 text-xs font-normal bg-green-200 dark:bg-black rounded" style="padding: 2px 6px;">
                    {{ item.year }}
                </div>
                <div class="ml-auto text-xs font-light opacity-50 hidden">{{ item.id }}</div>
                <component :is="sourceLogo" class="ml-auto opacity-80"></component>
            </div>
            <div class="actor text-gray-500">
                {{ item.area && item.area != "" ? item.area : "未知" }} / {{
                    item.director && item.director != "" ?
                        item.director : "未知"
                }}/ {{ item.lang && item.lang != "" ? item.lang : "未知" }}
            </div>
            <div class="actor text-sm text-slate-600 dark:text-slate-400">{{ item.actor }}</div>
            <div class="mt-auto des" v-html="item.des">
            </div>
            <div class="mt-auto flex space-x-2 items-center">
                <div class="cursor-pointer py-1 pl-4 pr-5 bg-amber-500 flex items-center"
                    style="border-radius: 1rem .5rem .5rem 1rem;" @click="changeVideo(0)">
                    <carbon:play-filled-alt class="h-4 w-4 text-white inline-block mr-1"></carbon:play-filled-alt>
                    <span class=" text-white">立即播放</span>
                </div>
                <div class="cursor-pointer border bg-zinc-300 dark:bg-zinc-800 text-amber-600 text-smborder-gray-300  dark:border-opacity-30 dark:border-violet-300"
                    @click="toinfo"
                    style="border-radius: .3rem .7rem .7rem .3rem; padding: 0.35rem 2rem 0.35rem 1.5rem;">查看详情</div>
            </div>
        </div>
        <div class="clear-both"></div>
    </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useVideoStore } from './videoStore'

import iqiyilogo from "../assets/iqiyi.vue"
import qqlogo from "../assets/qqvideo.vue"

export default {
    props: {
        item: Object,
    },
    name: 'VideoItem',
    setup(props, context) {

        var videoStore = useVideoStore()

        const series = computed(() => {
            let _series = []
            // name$url$siteinfo#{ next item }
            if (Object.keys(props.item).length == 0) { return _series }
            props.item.url.split('#').forEach(movieUrl => {
                let serie = {};
                serie.name = movieUrl.split('$')[0];
                serie.url = movieUrl.split('$')[1];
                serie.source = movieUrl.split('$')[2];
                _series.push(serie)
            });
            return _series
        })

        const changeVideo = (index) => {
            videoStore.videoItem = JSON.parse(JSON.stringify(props.item));
            videoStore.playerOptions.poster = videoStore.videoItem.pic;
            videoStore.playerOptions.name = videoStore.videoItem.name + " " + series.value[index].name;
            if (series.value[index].source == 'qq' ||
                series.value[index].source == 'qiyi') {
                videoStore.playerOptions.iframeSrc = "https://okjx.cc/?url=" + series.value[index].url;
                videoStore.playerOptions.src = '';
            } else {
                videoStore.playerOptions.iframeSrc = '';
                videoStore.playerOptions.src = series.value[index].url;
            }
            videoStore.showing = 'player'
            setTimeout(() => {
                document.getElementsByClassName('demo-player')[0].scrollIntoView({ block: "center" });
            }, 10)
        }

        const toinfo = () => {
            videoStore.videoItem = JSON.parse(JSON.stringify(props.item));
            videoStore.showing = 'info';
        }

        const sourceLogo = computed(() => {
            if (series.value[0].source == 'qiyi') {
                return iqiyilogo
            }
            if (series.value[0].source == 'qq') {
                return qqlogo
            }
            return undefined
        })
        return { changeVideo, toinfo, sourceLogo }
    }
}
</script>

<style scoped>
.movie-item {
    display: flex;
    margin-bottom: 3rem;
    margin-top: 2.5rem;
}

.movie-item .cover {
    position: relative;
    width: 180px;
    overflow: hidden;
    background: #000;
    margin: -1.5rem 0 .5rem .5rem;
    border-radius: .5rem;
    float: left;
}

.movie-item .cover img:hover {
    opacity: .9;
    transform: scale(1.25, 1.25);
}

.movie-item .cover img {
    width: 100%;
    transition: transform ease .25s;
    aspect-ratio: 166/242;
}

.movie-item .cover .duration {
    position: absolute;
    right: 5px;
    bottom: 5px;
    padding: 3px 6px;
    line-height: 1.2em;
    background-color: rgba(0, 0, 0, .65);
    color: #fff;
    font-size: 12px;
    border-radius: 2px;
}

.movie-item .detail>div {
    margin-bottom: .6rem;
}

.movie-item .detail .title {
    font-size: 1.3rem;
    font-weight: 600;
}

.movie-item .detail .date,
.movie-item .detail .author {
    font-size: .9rem;
    font-weight: 500;
}

.movie-item .detail .data.hot {
    background-color: #ff6060;
}

.ww {
    width: 4rem;
}

.des {
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: -o-ellipsis-lastline;
    text-overflow: ellipsis;
    word-break: break-word;
    -webkit-line-clamp: 2;
}

.actor {
    display: -webkit-box;
    overflow: hidden;
    -webkit-box-orient: vertical;
    text-overflow: -o-ellipsis-lastline;
    text-overflow: ellipsis;
    word-break: break-word;
    -webkit-line-clamp: 1;
}
</style>

