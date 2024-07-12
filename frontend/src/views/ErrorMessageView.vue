<script lang="ts" setup>

// Received properties
const props = defineProps({
  errorMessage: {
    type: String,
    required: true
  }
});

console.log(props);
</script>

<template>
<div class="errors-container flex items-center justify-center">
    <div class="errors-text">
    <h2>{{ props.errorMessage }}</h2>
    <router-link to="/">
        {{ $t('go_home') }}
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right-short" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M4 8a.5.5 0 0 1 .5-.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5A.5.5 0 0 1 4 8"/>
        </svg>
    </router-link>
    </div>
</div>
</template>
<style scoped lang="scss">
    @import '@/assets/styles/general/_general.index.scss';
    .errors-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 80px;
        min-height: 70vh;

        .errors-text {
            text-align: center;

            h1 {
            font-family: $font-2;
            font-size: 55px;
            font-weight: 200;
            color: $color-black;
            }

            h2 {
            position: relative;
            font-family: $font-5;
            font-size: 21px;
            font-weight: 500;
            color: $color-black;

            &::after {
                display: block;
                content: '';
                position: absolute;
                left: 50%;
                margin-top: 30px;
                margin-left: -65px;
                width: 130px;
                height: 2px;
                background-color: $color-blue;
            }
            }

            a {
                display: flex;
                justify-content: space-between;
                margin: 70px auto 0;
                padding: 2px 15px;
                width: 250px;
                max-width: 100%;
                border-radius: 6px;
                line-height: 40px;
                text-align: center;
                text-decoration: none;
                font-family: $font-5;
                font-size: 14px;
                font-weight: 400;
                background-color: $color-black;
                color: #ffffff;

                &:hover {
                    background-color: rgba($color: $color-black, $alpha: 0.7);
                }
                
                svg {
                    margin-top: 6px;
                    width: 25px;
                    height: 25px;
                }

            }
        }

    }
</style>