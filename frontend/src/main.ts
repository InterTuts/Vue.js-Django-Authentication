// System Utils
import { createApp } from 'vue';

// Installed Utils
import 'vuetify/styles'
import { createI18n } from 'vue-i18n';
import { createHead } from '@vueuse/head';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { createPinia } from 'pinia';

// App Utils
import en from './lang/en-US.json';
import App from './App.vue';
import router from './router';
import userPlugin from './plugins/userPlugin';
import axios from './axios';

// Material Icons
import '@mdi/font/css/materialdesignicons.css';


// Create a i18n instance
const i18n = createI18n({
    legacy: false,
    locale: "en",
    messages: {
      en
    }
});

// Create Vuetify instance
const vuetify = createVuetify({
  components,
  directives
});

// Create Vue instance
const app = createApp(App);

// Add axios instance
app.config.globalProperties.$axios = axios;

// Add router to Vue
app.use(router);

// Add pinia to Vue
app.use(createPinia());

// Add Vuetify to Vue
app.use(vuetify);

// Add i18 to vue
app.use(i18n);

// Add the user's plugin in Vue instance
app.use(userPlugin);

// Add VueUse Head to vue
app.use(createHead())

// Mount the Vue instance in DOM
app.mount('#app');
