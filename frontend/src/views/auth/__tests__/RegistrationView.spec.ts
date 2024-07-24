// System Utils
import { h } from 'vue';

// Installed Utils
import {
    mount,
    VueWrapper
} from '@vue/test-utils';
import {
    vi,
    describe,
    it,
    expect,
    beforeAll,
    afterAll
  } from 'vitest';
import { VApp } from "vuetify/components";

// App Utils
import RegistrationView from '../RegistrationView.vue';
import { useAuth } from "@/composables/useAuth";
import axios, { type Axios } from '@/axios';

// Create a mock for axios
vi.mock('axios', async () => {
  const actual = await vi.importActual<typeof Axios>('axios')
  return {
    ...actual
  }
});

describe('RegistrationForm.vue', () => {
  let wrapper: VueWrapper;

  beforeAll(() => {
    wrapper = mount(VApp, {
      slots: {
        default: h(RegistrationView),
      }
    });
  });

  afterAll(() => {
    wrapper.unmount();
  });

  it('renders the strings correctly', () => {
    expect(wrapper.text()).toContain('Sign Up to MyApp');
    expect(wrapper.text()).toContain('Continue with Google');
    expect(wrapper.text()).toContain('Do you have an account?');
    expect(wrapper.text()).toContain('Sign In');
  });

  it('renders the vuetify inputs', async () => {
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    expect(emailInput.exists()).toBeTruthy();
    expect(passwordInput.exists()).toBeTruthy();
  });

  it('validates form fields', async () => {
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    await emailInput.setValue('invalid email');
    await passwordInput.setValue('short');
    await wrapper.find('form').trigger('submit.prevent');
    expect(wrapper.text()).toContain('The email address is not valid.');
    expect(wrapper.text()).toContain('The password is too short.');
  });

  it('sends registration request', async () => {

    // Create a mock response
    const mockResponse = {
      data: { success: true, content: {}, message: 'Success' }
    };    

    // Set the mock response as axios response
    const mockAxiosPost = vi.fn().mockResolvedValue(mockResponse);

    // Replace the axios.post function with the mock
    axios.post = mockAxiosPost;

    // Arrange
    const { authRequest, successMessage, errorMessage, isLoading } = useAuth();

    // Try to sign up
    const response = await authRequest('api/auth/registration', { email: 'test@example.com', password: 'test' });

    // Verify if the response has expected values
    expect(isLoading.value).toBe(false);
    expect(successMessage.value).toBe('Success');
    expect(errorMessage.value).toBe('');
    expect(response).toEqual(mockResponse.data);
  });  

});