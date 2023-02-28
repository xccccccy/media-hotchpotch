<template>
    <div v-show="!isHidden"
        class="fixed top-0 left-0 header-container bg-slate-200 bg-opacity-50 dark:bg-zinc-900 dark:bg-opacity-50 shadow dark:shadow-zinc-800">
        <div class="header w-full sm:w-3/4 2xl:w-2/3 mx-auto">
            <HeaderHome :homeSetting="homeSetting"></HeaderHome>
            <component v-for="(headerSetting, index) in leftHeaderSettings" :is="headers[headerSetting.type]" class=" py-2 sm:py-4 min-w-fit flex"
                v-show="!headerSetting.hidden" @click="activateHeaderOfIndex(index, headerSetting.type)" :key="index"
                :class="{ headeractivate: headeractivate[index] }" :headerSetting="headerSetting"></component>
            <div style="margin-left: auto;"></div>
            <component v-for="(headerSetting, index) in rightHeaderSettings" :is="headers[headerSetting.type]" class="flex"
                v-show="!headerSetting.hidden" :key="index" :headerSetting="headerSetting"></component>
            <DrakMode @darkModeChange="darkModeChange" class="mx-3 flex"></DrakMode>
            <User @userLog="userLog" class="mx-3 flex"></User>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, watch, reactive, computed } from 'vue'
import axios from 'axios';
import DrakMode from '../foundation/DrakMode.vue';
import User from '../foundation/User.vue'
import HeaderHome from './headerHome.vue'
import CommonHeader from './commonHeader.vue'
import SearchHeader from './searchHeader.vue'

export default {
    name: "Header",
    props: {
        headerSetting: {
            type: Object,
            default: {}
        }
    },
    setup(props, context) {

        const headers = {
            common: CommonHeader,
            search: SearchHeader
        }

        const isHidden = computed(() => {
            if (props.headerSetting.hiddenSetting) {
                return props.headerSetting.hiddenSetting
            }
            return false
        })

        const homeSetting = computed(() => {
            if (props.headerSetting.homeSetting) {
                return props.headerSetting.homeSetting
            }
            return {
                homeString: 'Home',
                homeHref: '/'
            }
        })

        const headerSettings = computed(() => {
            if (props.headerSetting.headerSettings) {
                return props.headerSetting.headerSettings
            }
            return []
            // // [
            //     {
            //         type: 'search',
            //         placeholder: "搜索书籍。",
            //         clickHandle: (search_string) => {
            //             console.log('asdfgh', search_string)
            //         },
            //         position: "right" 
            //     },
            //     {
            //         type: 'common',
            //         headerString: '书架',
            //         class: ['student', 'asda']
            //     },
            //     {
            //         type: 'common',
            //         headerString: '书架2',
            //         clickHandle: () => {
            //             console.log('asdfgh')
            //         },
            //         hidden: true,
            //     },
            //     {
            //         type: 'common',
            //         headerString: 'Shǎng',
            //         clickHandle: () => {
            //             console.log('asdfgh')
            //         },
            //         style: "font-weight: 500; color: #CD9D02"
            //     }
            // ]
        })

        const headeractivate = reactive({})

        const rightHeaderSettings = computed(() => {
            let headerSettings = props.headerSetting.headerSettings ? props.headerSetting.headerSettings : []
            return headerSettings.filter((value) => value.position == "right")
        })

        let activeFlag = true;
        const leftHeaderSettings = computed(() => {
            let headerSettings = props.headerSetting.headerSettings ? props.headerSetting.headerSettings : []
            let leftHeaders = headerSettings.filter((value) => value.position != "right")
            if (leftHeaders.length && activeFlag) { 
                activeFlag = false;
                activateHeaderOfIndex(0, leftHeaders[0].type);
             }
            return headerSettings.filter((value) => value.position != "right")
        })

        const activateHeaderOfIndex = (index, type) => {
            for (let key in headeractivate) {
                headeractivate[key] = false
            }
            if (type != 'common') return;
            headeractivate[index] = true
        }

        const darkModeChange = computed(() => {
            if (props.headerSetting.darkmodeSetting) {
                return props.headerSetting.darkmodeSetting.darkModeChangeHandle
            }
            return () => {
                // console.log('darkMode Change.')
            }
        })

        const userLog = computed(() => {
            if (props.headerSetting.userSetting) {
                return props.headerSetting.userSetting.userLogHandle
            }
            return (mode) => {
                // console.log(mode, 'user loged.')
            }
        })

        return { homeSetting, headerSettings, leftHeaderSettings, rightHeaderSettings, headers, activateHeaderOfIndex, headeractivate, userLog, darkModeChange, isHidden };
    },
    components: { DrakMode, User, HeaderHome }
}

</script>

<style scoped>
.header-container {
    /* position: fixed;
    top: 0;
    left: 0; */
    width: 100%;
    /* box-shadow: 2px -2px 10px #00000058; */
    backdrop-filter: blur(25px);
    z-index: 99;
}

.header {
    display: flex;
}

.header>div {
    cursor: pointer;
    align-items: center;
}

.header>div:hover {
    /* padding-bottom: calc(0.3rem - 2px); */
    border-bottom: 2px solid rgb(218, 175, 0);
}

.headeractivate {
    font-weight: 700 !important;
    border-bottom: 2px solid rgb(20, 175, 103);
}
</style>