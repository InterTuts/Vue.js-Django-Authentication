// System Utils
import { h } from "vue";

// Installed Utils
import { type VueWrapper, mount } from "@vue/test-utils";
import { 
    vi,
    afterAll,
    beforeAll,
    describe,
    expect,
    it
} from "vitest";
import { VApp } from "vuetify/components";

// App Utils
import ResetPasswordView from '../ResetPasswordView.vue';
import axios, { type Axios } from '@/axios';
import { useAuth } from "@/composables/useAuth";

// Create a mock for axios
vi.mock('axios', async () => {
  const actual = await vi.importActual<typeof Axios>('axios')
  return {
    ...actual
  }
});

describe('ResetPasswordView.vue', () => {
    let wrapper: VueWrapper;

    beforeAll(() => {
        wrapper = mount(VApp, {
            slots: {
              default: h(ResetPasswordView),
            }
        });
    });

    afterAll(() => {
        wrapper.unmount();
    });

    it('renders the strings correctly', () => {
        expect(wrapper.text()).toContain('Reset Password');
        expect(wrapper.text()).toContain('Do you remember the password?');
        expect(wrapper.text()).toContain('Sign In');
    });

    it('renders email input correctly', () => {
        const emailInput = wrapper.find('input[type="email"]');
        expect(emailInput.exists()).toBeTruthy();
    });

    it('validates email input', async () => {
        const emailInput = wrapper.find('input[type="email"]');
        await emailInput.setValue('invalid email');
        await wrapper.find('form').trigger('submit.prevent');
        expect(wrapper.text()).toContain('The email address is not valid.');
    });

    it('requests password reset', async () => {

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
    
        // Try to request password reset
        const response = await authRequest('api/auth/registration', { email: 'test@example.com' });
    
        // Verify if the response has expected values
        expect(isLoading.value).toBe(false);
        expect(successMessage.value).toBe('Success');
        expect(errorMessage.value).toBe('');
        expect(response).toEqual(mockResponse.data);

    });

});