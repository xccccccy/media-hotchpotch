<template>
    <div>
        <div class="mt-2 mb-8">
            <span class="text-xl font-bold">Book</span>
            <div class="py-4">
                <el-button @click="initRecommendBookInfo">初始化推荐书籍</el-button>
            </div>
            <div class="my-2 p-2 border border-zinc-300 dark:border-zinc-500">
                <el-table :data="recommendBookInfotableData" style="width: 100%; font-size: 15px;">
                    <el-table-column prop="bookSource" label="推荐源网址" width="200" />
                    <el-table-column prop="recommendBook" label="推荐booksJson" width="200" />
                    <el-table-column prop="lastUpdateTime" label="最后更新时间" />
                </el-table>
            </div>
        </div>
        <div class="my-8 h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500"></div>
        <div>
            <span class="text-xl font-bold">Video</span>
            <div class="flex items-center">
                <div class="pr-6">资源网资源</div>
                <el-checkbox-group v-model="urlName.private" size="large" class="my-4">
                    <el-checkbox-button v-for="item in urlNames.private" :key="item" :label="item" :value="item">
                        {{ item }}
                    </el-checkbox-button>
                </el-checkbox-group>
            </div>
            <div v-for="(value, key) in urlNames.official" :key="key" class="flex items-center">
                <div class="pr-6">{{ key }}</div>
                <el-checkbox-group v-model="urlName.official[key]" size="large" class="my-4">
                    <el-checkbox-button v-for="item in urlNames.official[key]" :key="item" :label="item" :value="item">
                        {{ item }}
                    </el-checkbox-button>
                </el-checkbox-group>
            </div>

            <el-button @click="initDownloadVideos">初始化视频数据库</el-button>
            <el-button @click="delDownloadVideos">删除视频数据库所有数据</el-button>
            <div class="my-5 p-2 border border-zinc-300 dark:border-zinc-500">
                <el-table :data="videoCmsInfos" style="width: 100%; font-size: 15px;">
                    <el-table-column prop="name" label="源网址名称" width="200" />
                    <el-table-column prop="isOfficial" label="是否官方资源" width="200" />
                    <el-table-column prop="resourcesNums" label="资源数量" width="200" />
                    <el-table-column prop="lastUpdateTime" label="最后更新时间" />
                </el-table>
            </div>
        </div>
        <div class="my-8 h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500"></div>
    </div>
</template>

<script>
import { ref, reactive } from "vue"
import { initVideoDatabase, initUrlNames, delAllVideos, initRecommendBookCmsInfo, getAllVideoCmsInfo, getRecommendBookCmsInfo } from "../foundation/api/cmsapi"

export default {
    name: "CMS",
    setup() {
        const urlName = ref({ "private": [], "official": {} })
        const urlNames = ref({ "private": [], "official": {} })
        const initUrlName = () => {
            initUrlNames()
                .then((res) => {
                    urlNames.value = res.data.data;
                })
                .catch((err) => {
                    ElNotification({ message: "ERROR!", type: 'error', duration: 2500 });
                })
        }
        initUrlName()

        const initDownloadVideos = () => {
            const downloadLoading = ElLoading.service({ fullscreen: true, lock: true, text: '正在下载。。。' })
            initVideoDatabase(urlName.value)
                .then((res) => {
                    ElNotification({ message: res.data, type: 'success', duration: 2500 });
                })
                .catch((err) => {
                    ElNotification({ message: "ERROR!", type: 'error', duration: 2500 });
                })
                .finally(() => {
                    downloadLoading.close()
                })
        }

        const delDownloadVideos = () => {
            const delLoading = ElLoading.service({ fullscreen: true, lock: true, text: '正在删除' })
            delAllVideos()
                .then((res) => {
                    console.log(res);
                    ElNotification({ message: res.data, type: 'success', duration: 2500 });
                })
                .catch((err) => {
                    ElNotification({ message: "ERROR!", type: 'error', duration: 2500 });
                })
                .finally(() => {
                    delLoading.close()
                })
        }

        const initRecommendBookInfo = () => {
            const recommendLoading = ElLoading.service({ fullscreen: true, lock: true, text: '正在初始化推荐书籍' })
            initRecommendBookCmsInfo()
                .then((res) => {
                    console.log(res);
                    ElNotification({ message: res.data, type: 'success', duration: 2500 });
                })
                .catch((err) => {
                    ElNotification({ message: "ERROR!", type: 'error', duration: 2500 });
                })
                .finally(() => {
                    recommendLoading.close()
                })
        }
        const videoCmsInfos = ref([
            {
                lastUpdateTime: '2016-05-03',
                name: 'Tom',
                resourcesNums: '23323',
                isOfficial: '是'
            }
        ])

        getAllVideoCmsInfo().then((res) => {
            console.log(res.data.videoCmsInfos)
            videoCmsInfos.value = res.data.videoCmsInfos;
        })

        const recommendBookInfotableData = ref([
            {
                lastUpdateTime: '2016-05-03',
                bookSource: 'Tom',
                recommendBook: 'No. 189, Grove St, Los Angeles',
            }])

        getRecommendBookCmsInfo().then((res) => {
            console.log(res.data)
            let recommendBookCmsInfos = res.data.recommendBookCmsInfos;
            recommendBookCmsInfos = recommendBookCmsInfos.map((item, index) => {
                let obj = item
                obj.recommendBook = obj.recommendBook?.slice(0, 20);
                return obj
            })
            console.log(recommendBookCmsInfos)
            recommendBookInfotableData.value = recommendBookCmsInfos;
        })

        return { initDownloadVideos, urlNames, urlName, delDownloadVideos, initRecommendBookInfo, videoCmsInfos, recommendBookInfotableData }
    }

}
</script>

<style>
.el-table .warning-row {
    --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
    --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>