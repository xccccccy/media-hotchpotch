<template>
    <div @click="headerSetting.clickHandle" :class="headerSetting.class" class="mx-2 sm:mx-6">
        <component :is="headerSetting.iconSetting" class="h-6 w-6 text-indigo-600"/>
        <span :style="headerSetting.style">{{ headerSetting.headerString }}</span>
    </div>
</template>

<script>

export default {
    name: "CommonHeader",
    props: {
        headerSetting: {
            type: Object,
            default: {
                clickHandle: {
                    type: Function,
                    default: () => {
                        console.log('qwerty')
                    }
                },
                myClass: {
                    type: String,
                    default: '/'
                },
                headerString: {
                    type: String,
                    default: '默认Header'
                }
            }
        },

    },
    setup() {

        return {};
    }
}

</script>

<style scoped>
</style>