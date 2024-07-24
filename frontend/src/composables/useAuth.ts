// System Utils
import { ref } from 'vue';

// Installed Utils
import DOMPurify from 'dompurify';

// App Utils
import type { BaseUser, BaseUserEmail } from '@/interfaces/user';
import type ApiResponse from '@/interfaces/apiResponse';
import axios, { type AxiosResponse } from '@/axios';

export const useAuth = () => {
  // Reactive reference for success messages
  const successMessage = ref('');

  // Reactive reference for error message
  const errorMessage = ref('');

  // Loading marker
  const isLoading = ref<boolean>(false);

  // Sign in or register a user
  const authRequest = async (
    url: string,
    user: BaseUser | BaseUserEmail
  ): Promise<ApiResponse<null>> => {
    // Enable the loading
    isLoading.value = true;

    // Reset the error and success message
    successMessage.value = errorMessage.value = '';

    try {
      // Send request
      const response: AxiosResponse<ApiResponse<null>> = await axios.post(
        url,
        user
      );

      // Check if the message is success
      if (response.data.success) {
        // Set Message
        successMessage.value = DOMPurify.sanitize(response.data.message);
      } else {
        // Set Message
        errorMessage.value = DOMPurify.sanitize(response.data.message);
      }

      return response.data;
    } catch (error) {
      // Set error
      errorMessage.value =
        error instanceof Error ? error.message : 'An error has occurred.';
      throw error;
    } finally {
      // Disable the loading
      isLoading.value = false;
    }
  };

  return { authRequest, successMessage, errorMessage, isLoading };
}
