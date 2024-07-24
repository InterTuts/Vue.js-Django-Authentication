// Installed Utils
import axios, { type AxiosResponse, Axios } from 'axios';

// App Utils
import { useToken } from '@/composables/useToken';

// Create an instance for axios
const instance = axios.create({
    baseURL: import.meta.env.VITE_APP_API_URL
});

// Set the token in the header
instance.interceptors.request.use((config) => {
    // Get the user's token
    const { token } = useToken();
    // Verify if user's token exists
    if ( token.value ) {
        config.headers.Authorization = `Token ${token.value}`;
    }
    return config;
},
(error) => {
    return Promise.reject(error);
});

export type { AxiosResponse, Axios };
export default instance;