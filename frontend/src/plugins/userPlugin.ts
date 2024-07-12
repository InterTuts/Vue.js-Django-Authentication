// App Utils
import { useUserStore } from '@/stores/useUserStore';

export default {
  install: () => {
    // Get the user store
    const userStore = useUserStore();
    // Get the user's data when the plugin is installed
    userStore.fetchUserData();
  }
}
