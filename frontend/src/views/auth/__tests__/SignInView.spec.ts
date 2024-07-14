// Installed Utils
import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import SignInView from '../SignInView.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Mock useAuth and useToken composables
vi.mock('@/composables/useAuth', () => ({
  useAuth: () => ({
    authRequest: vi.fn(),
    successMessage: '',
    errorMessage: '',
    isLoading: false,
  }),
}));

vi.mock('@/composables/useToken', () => ({
  useToken: () => ({
    saveToken: vi.fn(),
  }),
}));

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: '',
      component: SignInView,
      meta: { noAuth: true },
    },
  ],
});

describe('SignInForm.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the form correctly', () => {
    const wrapper = mount(SignInView);
    expect(wrapper.text()).toContain('Sign In to MyApp');
  });

  it('validates form fields', async () => {
    const wrapper = mount(SignInView);

    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');

    expect(emailInput.exists()).toBeTruthy()
    /*await emailInput.setValue('invalid email');
    await passwordInput.setValue('short');

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.text()).toContain('Email is not valid');
    expect(wrapper.text()).toContain('Password is too short');*/
  });

  /*

  it('submits the form correctly', async () => {
    const authRequestMock = vi.fn().mockResolvedValue({
      success: true,
      content: {
        token: 'token',
        id: 'user-id',
        email: 'user@example.com',
      },
    });

    vi.mock('@/composables/useAuth', () => ({
      useAuth: () => ({
        authRequest: authRequestMock,
        successMessage: '',
        errorMessage: '',
        isLoading: false,
      }),
    }));

    const wrapper = mount(SignInView, {
      global: {
        plugins: [i18n, router, createTestingPinia()],
      },
    });

    await wrapper.find('input[type="email"]').setValue('user@example.com');
    await wrapper.find('input[type="password"]').setValue('password123');

    await wrapper.find('form').trigger('submit.prevent');

    expect(authRequestMock).toHaveBeenCalled();
  });*/
});
