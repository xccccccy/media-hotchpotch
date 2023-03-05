<template>
    <div class="footer text-zinc-300 font-bold text-tiny" v-show="footer_show">
        <div class="h-0.5 bg-gradient-to-r from-yellow-500 via-pink-500 to-cyan-500 w-full"></div>
        <div class="py-5">
            <div>
                <a href="http://beian.miit.gov.cn/">
                    <span>京ICP备2022006333号</span>
                </a>
            </div>
            <div>
                <span>
                    Copyright © 2023 By
                    <a href="http://www.xcya.cn" class="italic font-bold text-xl bg-clip-text linear-gradient inverse text-fill-transparent">
                        Silver alien
                    </a>
                </span>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Footer",
    props: {
        footer_show: {
            type: Boolean,
            default: true
        }
    },
    setup() {

        return {};
    }
}

</script>

<style scoped>
.footer {
    /* position:absolute;
    bottom:0%; */
    width: 100%;
    text-align: center;
    backdrop-filter: blur(20px);
    background: #0000009C;
}
</style>