<script setup lang="ts">
// System Utils
import { reactive } from 'vue';

// Installed Utils
import { useI18n } from 'vue-i18n';
import { useHead } from '@vueuse/head';
import { useVuelidate } from '@vuelidate/core';
import { required, email, helpers } from '@vuelidate/validators';

// App Utils
import { useAuth } from '@/composables/useAuth';

// Get i18n functions
const { t } = useI18n();

// Set page title and description
useHead({
  title: t('reset_password'),
  meta: [
    { name: 'description', content: () => t('reset_password_page_description') },
    { name: 'keywords', content: () => 'reset, password, account, page' }
  ]
});

// Default fields value
const initialState = {
  email: ''
}

// Make the fields reactive
const state = reactive({
  ...initialState
});

// Rules for Vuelidate
const rules = {
  email: {
    required: helpers.withMessage(t('email_short'), required),
    email: helpers.withMessage(t('email_not_valid'), email)
  }
}

// Configure Vuelidate
const v$ = useVuelidate(rules, state);

// Use auth variables
const { authRequest, successMessage, errorMessage, isLoading } = useAuth();

// Handle the form submit
const handleSubmit = async () => {

  // Verify if errors exists
  if (v$.value.$invalid) {
    return;
  }
console.log(state);
  // Request the password reset
  const passwordReset = authRequest('api/auth/password-reset', state);
  
  // Process the promise response
  passwordReset.then(response => {
    console.log(response);
  })
  .catch(error => {
    console.log(error);
  });

};

</script>
<template>
  <v-main>
    <v-container>
      <form @submit.prevent="handleSubmit">
        <v-row>
          <v-col cols="12">
            <h3>{{ $t('reset_password') }}</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="state.email"
              :error-messages="v$.email.$errors.map((e) => e.$message)"
              :label="$t('email')"
              required
              variant="outlined"
              autocomplete="new-email"
              @blur="v$.email.$touch"
              @input="v$.email.$touch"
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
                {{ $t('reset') }}
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
