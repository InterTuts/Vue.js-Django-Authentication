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
import { usePassword } from '@/composables/usePassword';

// Get i18n functions
const { t } = useI18n();

// Set page title and description
useHead({
  title: t('change_password'),
  meta: [
    { name: 'description', content: () => t('change_password_page_description') },
    { name: 'keywords', content: () => 'change, password, account, page' }
  ]
});

// Default fields value
const initialState = {
  password: '',
  repeat_password: ''
}

// Rules for Vuelidate
const rules = {
  password: {
    required: helpers.withMessage(t('password_short'), required),
    minLength: helpers.withMessage(t('password_short'), minLength(8)),
    maxLength: helpers.withMessage(t('password_long'), maxLength(20))
  },
  repeat_password: {
    required: helpers.withMessage(t('password_short'), required),
    minLength: helpers.withMessage(t('password_short'), minLength(8)),
    maxLength: helpers.withMessage(t('password_long'), maxLength(20))
  }
}

// Make the fields reactive
const state = reactive({
  ...initialState
});

// Configure Vuelidate
const v$ = useVuelidate(rules, state);

// Use reactive variables
const { updateRequest, successMessage, errorMessage, isLoading } = usePassword();

// Use the router
const router = useRouter();

// Timeout ID for cleanup
let timeoutId;

// Handle the form submit
const handleSubmit = async () => {

  // Reset error message
  errorMessage.value = '';

  // Verify if errors exists
  if (v$.value.$invalid) {
    return;
  }

  // Check if the password doesn't match
  if ( state.password !== state.repeat_password ) {
    errorMessage.value = t('repeat_password_doesnt_match');
    return;
  }

  // Get the token
  const token = router.currentRoute.value.params.token;

  // Change the password
  const signIn = updateRequest('api/auth/change-password', {
    token: token,
    password: state.password
  });

  // Process the promise response
  signIn.then(response => {

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

</script>
<template>
  <v-main>
    <v-container>
      <form @submit.prevent="handleSubmit">
        <v-row>
          <v-col cols="12">
            <h3>{{ $t('create_new_password') }}</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              type="password"
              v-model="state.password"
              :counter="20"
              :error-messages="v$.password.$errors.map((e) => e.$message)"
              :label="$t('new_password')"
              variant="outlined"
              autocomplete="new-password"
              @blur="v$.password.$touch"
              @input="v$.password.$touch"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              type="password"
              v-model="state.repeat_password"
              :counter="20"
              :error-messages="v$.repeat_password.$errors.map((e) => e.$message)"
              :label="$t('repeat_password')"
              variant="outlined"
              autocomplete="repeat-password"
              @blur="v$.repeat_password.$touch"
              @input="v$.repeat_password.$touch"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn
                type="submit"
                class="auth-btn"
                @click="v$.$validate"
                :class="{'auth-submitting-active-btn': isLoading }">
                {{ $t('save') }}
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
                {{ $t('do_you_remember_password') }}
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
