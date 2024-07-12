// Installed Utils
import { createRouter, createWebHistory } from 'vue-router';
import DOMPurify from 'dompurify';

// App Utils
import { useToken } from '@/composables/useToken';
import { useUserStore } from '@/stores/useUserStore';
import { useSocialStore } from '@/stores/useSocialStore';
import AuthLayout from '../layouts/AuthLayout.vue';
import SignInView from '../views/auth/SignInView.vue';
import RegistrationView from '../views/auth/RegistrationView.vue';
import ResetPasswordView from '../views/auth/ResetPasswordView.vue';
import ChangePasswordView from '../views/auth/ChangePasswordView.vue';
import GoogleConnectView from '../views/auth/GoogleConnectView.vue';
import MainView from '../views/dashboard/MainView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      component: AuthLayout,
      children: [
        { path: '', component: SignInView, meta: { noAuth: true } },
        { path: 'registration', component: RegistrationView, meta: { noAuth: true } },
        { path: 'reset-password', component: ResetPasswordView, meta: { noAuth: true } },
        { path: 'change-password/:token', component: ChangePasswordView, meta: { noAuth: true } },
        {
          path: 'google/connect',
          component: GoogleConnectView,
          meta: { socialAuth: true },
          props: (route) => ({
            failedMessage: route.meta.failedMessage || undefined
          })
        }
      ]
    },
    {
      path: '/dashboard',
      component: MainView,
      meta: { requiresAuth: true }
    },
    {
      path: '/logout',
      component: { template: '<div></div>' },
      beforeEnter: (to, from, next) => {
        // Get the user's store
        const userStore = useUserStore();
        // Logout
        userStore.logout();
        // Redirect to login
        next('/');
      }
    }
  ]
})

// Register an interceptor
router.beforeEach(async (to, from, next) => {
  // Get the user's token
  const { token, clearToken } = useToken();  
  // Verify if the user shouldn't be authenticated
  if (to.meta.noAuth) {
    // Verify if the token is saved
    if (token.value) {
      next('/dashboard');
      return;
    }
  } else if (to.meta.requiresAuth) {
    // Get the user's store
    const userStore = useUserStore();
    // Check if user's data exists
    if ( !userStore.userData ) {
      // Get the user data
      await userStore.fetchUserData();
    }
    // Chceck if user's data exists
    if (!userStore.userData) {
      // Delete the token
      clearToken();      
      // Redirect to login
      next('/');
    } else {
      next();
    }
    return;
  } else if (to.meta.socialAuth) {
    // Get the code
    const code = to.query.code || undefined;
    // Check if code exists
    if ( typeof code !== 'string' ) {
      // Set error message
      to.meta.failedMessage = 'The authorization code is missing.';
      next();
      return;      
    }
    // Get the social store
    const socialStore = useSocialStore();
    // Get the user's store
    const userStore = useUserStore();
    // Excange the code
    await socialStore.exchangeAuthorizationCode(DOMPurify.sanitize(code));
    // Chceck if error message exists exists
    if (socialStore.errorMessage) {
      to.meta.failedMessage = socialStore.errorMessage;
    }
    // Chceck if user's data exists
    if (userStore.userData) {
      next('/dashboard');
    } else {
      next();
    }
    return;
  }
  next();
})

export default router
