<script setup lang="ts">
// System Utils
import { reactive, onUnmounted } from 'vue';

// Installed Utils
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useHead } from '@vueuse/head';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, maxLength, helpers } from '@vuelidate/validators';

// App Utils
import { useSocial } from '@/composables/useSocial';
import { useSocialStore } from '@/stores/useSocialStore';

// Get the social store
const socialStore = useSocialStore();

// Get i18n functions
const { t } = useI18n();

// Set page title and description
useHead({
  title: t('sign_up'),
  meta: [
    { name: 'description', content: () => t('sign_up_page_description') },
    { name: 'keywords', content: () => 'sign, up, registration, page' }
  ]
});

// Default fields value
const initialState = {
  email: '',
  password: ''
}

// Make the fields reactive
const state = reactive({
  ...initialState
});

// Rules for Vuelidate
const rules = {
  password: {
    required: helpers.withMessage(t('password_short'), required),
    minLength: helpers.withMessage(t('password_short'), minLength(8)),
    maxLength: helpers.withMessage(t('password_long'), maxLength(20))
  }
}

// Configure Vuelidate
const v$ = useVuelidate(rules, state);

// Use social variables
const { authRequest, successMessage, errorMessage, isLoading } = useSocial();

// Use the router
const router = useRouter();

// Timeout ID for cleanup
let timeoutId;

// Handle the form submit
const handleSubmit = async () => {

  // Verify if errors exists
  if (v$.value.$invalid) {
    return;
  }

  // Register the user
  const register = authRequest('api/auth/social-registration', {
    social_id: socialStore.userData.social_id,
    email: socialStore.userData.email,
    password: state.password
  });

  // Process the promise response
  register.then(response => {
    // Check if response is successfully
    if ( response.success ) {
      // Wait for 2 seconds
      timeoutId = setTimeout(() => {
        router.push('/');
      }, 2000);    
    }
  }).catch (error => {
    console.log(error);
  });

};

// Cleanup on component unmount
onUnmounted(() => {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
});

// Received properties
const props = defineProps({
  failedMessage: {
    type: String,
    required: false
  }
});

// Check if user's data exists
if ( socialStore.userData ) {
  state.email = socialStore.userData.email;
}
</script>
<template>
  <v-main>
    <v-container>
      <form @submit.prevent="handleSubmit" v-if="!props.failedMessage">
        <v-row>
          <v-col cols="12">
            <h3>{{ $t('sign_up_to_my_app') }}</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="state.email"
              :label="$t('email')"
              variant="outlined"
              autocomplete="new-email"
              disabled
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              type="password"
              v-model="state.password"
              :counter="20"
              :error-messages="v$.password.$errors.map((e) => e.$message)"
              :label="$t('password')"
              variant="outlined"
              autocomplete="new-password"
              @blur="v$.password.$touch"
              @input="v$.password.$touch"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn type="submit" class="auth-btn" @click="v$.$validate" :class="{'auth-submitting-active-btn': isLoading }">
              {{ $t('sign_up') }}
              <span class="mdi mdi-arrow-right-bold auth-main-form-submit-icon"></span>
              <span class="mdi mdi-cached rotate-animation auth-main-form-submitting-icon"></span>
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div class="auth-main-form-alerts">
              <div
                class="auth-main-form-alert-success top-to-bottom-animation"
                role="alert"
                v-if="successMessage"
              >
                <span class="mdi mdi-bell-outline auth-main-form-alert-success-icon"></span>
                <p>{{ successMessage }}</p>
              </div>
              <div
                class="auth-main-form-alert-error top-to-bottom-animation"
                role="alert"
                v-else-if="errorMessage"
              >
                <span class="mdi mdi-bell-outline auth-main-form-alert-error-icon"></span>
                <p>{{ errorMessage }}</p>
              </div>
            </div>
          </v-col>
        </v-row>        
        <v-row>
          <v-col cols="12">
            <div class="auth-additional-link">
              <p>
                {{ $t('do_you_have_an_account') }}
                <router-link to="/" class="inline-block auth-main-form-reset-link">
                  {{ $t('sign_in') }}
                </router-link>
              </p>
            </div>
          </v-col>
        </v-row>
      </form>
      <v-row class="ma-0" v-else-if="props.failedMessage">
        <v-col cols="12">
          <div class="auth-main-form-alerts">
            <div
              class="auth-main-form-alert-error top-to-bottom-animation"
              role="alert"
            >
              <span class="mdi mdi-bell-outline auth-main-form-alert-error-icon"></span>
              <p>{{ props.failedMessage }}</p>
            </div>
          </div>
        </v-col>
      </v-row>       
    </v-container>
  </v-main>
</template>
<style>
@import '@/assets/styles/auth/_main.scss';
</style>
