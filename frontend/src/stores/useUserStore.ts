// Installed Utils
import { defineStore } from 'pinia';
import axios, { type AxiosResponse } from '@/axios';

// App Utils
import type ApiResponse from '@/interfaces/apiResponse';
import type { User } from '@/interfaces/user';
import { useToken } from '@/composables/useToken';

export const useUserStore = defineStore('user', {
  state: () => ({
    userData: null as User | null
  }),
  actions: {
    setUserData(data: User) {
      this.userData = data
    },
    async fetchUserData() {
      // Get the user's token
      const { token } = useToken();

      // Verify if the token is saved
      if (!token.value) {
        return
      }

      try {
        // Send request
        const response: AxiosResponse<ApiResponse<User>> = await axios.get('api/user/info');

        // Check if the message is success
        if (response.data.success) {
          this.setUserData(response.data.content as User);
        }
      } catch (error) {
        console.error(error);
      }
    },
    logout() {
      // Get the user's token
      const { clearToken } = useToken();
      
      // Delete the token
      clearToken();
      
      // Reset the store
      this.resetStore();
    },
    resetStore() {
      this.userData = null;
    }
  }
})