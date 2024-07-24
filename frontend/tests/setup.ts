// Installed Utils
import { config } from '@vue/test-utils';
import { vi } from 'vitest';
import { createTestingPinia } from '@pinia/testing';
import { createI18n } from 'vue-i18n';
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import ResizeObserver from 'resize-observer-polyfill';
import { createHead } from '@vueuse/head';

// App Utils
import en from '../src/lang/en-US.json';
import router from '../src/router/index';

if (typeof global !== 'undefined') {
  global.ResizeObserver = ResizeObserver;
}

// Create a Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
})

// Create a Vue I18n instance
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en
  }
});

// Register the plugins for unit tests
config.global.plugins = [
  createTestingPinia({
    createSpy: vi.fn
  }),
  i18n,
  vuetify,
  createHead(),
  router
];