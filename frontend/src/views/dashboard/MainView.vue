<script setup lang="ts">
// Installed Utils
import { useI18n } from 'vue-i18n';
import { useHead } from '@vueuse/head';

// Get i18n functions
const { t } = useI18n();

// Set page title and description
useHead({
  title: t('dashboard'),
  meta: [
    { name: 'description', content: () => t('dashboard_page_description') },
    { name: 'keywords', content: () => 'dashboard, account, registration, page' }
  ]
});

// App Utils
import { useUserStore } from '@/stores/useUserStore';


// Get the user store
const userStore = useUserStore();

</script>
<template>
    <div class="user-data" v-if="userStore.userData">
        <div class="user-info">
            <p>{{ $t('user_id') }}: {{ userStore.userData.id }}</p>
            <p>{{ $t('email') }}: {{ userStore.userData.email }}</p>
        </div>
        <div class="user-actions">
            <p>
                <router-link to="/logout">
                    {{ $t('logout') }}
                </router-link>
            </p>
        </div>        
    </div>
</template>
<style scoped lang="scss">
    @import '@/assets/styles/general/_general.index.scss';
    .user-data {
        display: flex;
        margin: 50px auto;
        padding: 15px;
        width: 60%;
        min-height: 500px;
        border: 1px solid #DDD;
        font-family: $font-8;
        color: $color-black;
    }

    .user-info {
        width: 50%;
    }

    .user-info p {
        margin-bottom: 15px;
    }

    .user-actions {
        width: 50%;
        text-align: right;
    }

    .user-actions p a {
        text-decoration: none;
        font-family: $font-8;
        color: $color-blue;
    }

    .user-actions p a:hover {
        border-bottom: 1px solid $color-blue;
    }
</style>