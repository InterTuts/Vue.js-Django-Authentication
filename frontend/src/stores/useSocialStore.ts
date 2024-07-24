// Installed Utils
import DOMPurify from 'dompurify';
import { defineStore } from 'pinia';

// App Utils
import type ApiResponse from '@/interfaces/apiResponse';
import type { UserSocial, UserLogin } from '@/interfaces/user';
import axios, { type AxiosResponse } from '@/axios';
import { useToken } from '@/composables/useToken';
import { useUserStore } from '@/stores/useUserStore';

export const useSocialStore = defineStore('social', {
    state: () => ({
        userData: null as UserSocial | null,
        errorMessage: null as string | null
    }),
    actions: {
        async exchangeAuthorizationCode(code: string) {
            // Reset the social store
            this.resetStore();
            // Use the token methods
            const { saveToken, clearToken } = useToken();
            // Delete the token
            clearToken();
            // Get the user store
            const userStore = useUserStore();
            // Reset user's store
            userStore.resetStore();
            try {
                // Send request
                const response: AxiosResponse<ApiResponse<UserSocial & UserLogin>> = await axios.post('api/auth/google-code', {
                    code: code
                });
                // Check if the message is success
                if (response.data.success) {
                    if ( response.data.content && response.data.content.social_id ) {
                        this.userData = {
                            social_id: response.data.content.id,
                            email: DOMPurify.sanitize(response.data.content.email)
                        };
                    } else if ( response.data.content && response.data.content.id ) {
                        // Save the token
                        saveToken(DOMPurify.sanitize(response.data.content.token));
                        // Save User
                        userStore.setUserData({
                            id: response.data.content.id,
                            email: DOMPurify.sanitize(response.data.content.email)
                        });
                    }
                } else if (response.data.message) {
                    this.errorMessage = DOMPurify.sanitize(response.data.message);
                }

            } catch (error) {
                console.error(error);
            }
        },
        resetStore() {
            this.userData = null;
            this.errorMessage = null;
        }
    }
});