<script setup lang="ts">
// System Utils
import { reactive, onUnmounted } from 'vue';

// Installed Utils
import { useI18n } from 'vue-i18n';
import { useHead } from '@vueuse/head';
import { useRouter } from 'vue-router';
import { useVuelidate } from '@vuelidate/core';
import { required, email, minLength, maxLength, helpers } from '@vuelidate/validators';

// App Utils
import { useAuth } from '@/composables/useAuth';

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
})

// Rules for Vuelidate
const rules = {
  email: {
    required: helpers.withMessage(t('email_short'), required),
    email: helpers.withMessage(t('email_not_valid'), email)
  },
  password: {
    required: helpers.withMessage(t('password_short'), required),
    minLength: helpers.withMessage(t('password_short'), minLength(8)),
    maxLength: helpers.withMessage(t('password_long'), maxLength(20))
  }
}

// Configure Vuelidate
const v$ = useVuelidate(rules, state);

// Use auth variables
const { authRequest, successMessage, errorMessage, isLoading } = useAuth();

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
  const register = authRequest('api/auth/registration', state);

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

// Create google connect link
const googleConnect = import.meta.env.VITE_APP_API_URL + 'api/auth/google-connect';
</script>
<template>
  <v-main>
    <v-container>
      <form @submit.prevent="handleSubmit">
        <v-row>
          <v-col cols="12">
            <h3>{{ $t('sign_up_to_my_app') }}</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div>
              <a :href="googleConnect" class="auth-main-form-continue-google-link">
                <img src="/google.png" />
                {{ $t('continue_with_google') }}
              </a>
            </div>
            <div class="auth-main-form-separator" data-text="OR"></div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="state.email"
              :error-messages="v$.email.$errors.map((e) => e.$message)"
              :label="$t('email')"
              variant="outlined"
              autocomplete="new-email"
              @blur="v$.email.$touch"
              @input="v$.email.$touch"
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
    </v-container>
  </v-main>
</template>
<style>
@import '@/assets/styles/auth/_main.scss';
</style>
