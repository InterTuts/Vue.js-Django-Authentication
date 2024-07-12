// System Utils
import { ref } from 'vue';

// Installed Utils
import Cookies from 'js-cookie';

// Tokens Manager
export const useToken = () => {

    // Reactive token holder
    const token = ref(Cookies.get('userToken') || null);
    
    /**
     * Save token
     * 
     * @param newToken string
     */
    const saveToken = (newToken: string) => {

        // Update the reactive token holder
        token.value = newToken;

        // Save token
        Cookies.set('userToken', newToken, {
            secure: true,
            sameSite: 'strict'
        });
    }

    /**
     * Clear Token
     */
    const clearToken = () => {

        // Empty the reactive token holder
        token.value = '';

        // Remove access token
        Cookies.remove('userToken');
    }    

    return {
        token,
        saveToken,
        clearToken
    };

}