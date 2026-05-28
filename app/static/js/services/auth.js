import { api } from "./requests.js";

export const authApi = {
    // Логин - НЕ отправляем куки!
    login: (username, password) => {
        const formData = new URLSearchParams();
        formData.append("grant_type", "password");
        formData.append("username", username);
        formData.append("password", password);
        return api.post('/v1/auth/login', formData, { isFormData: true});
    },

    register: (username, password) => {
        return api.post('/v1/auth/register', { username: username, password: password });
    },
    
    refresh: () => {
        return api.post('/v1/auth/refresh', {});
    }
};


export const executeLoginFlow = async (username, password) => {
    try {
        const loginResult = await authApi.login(username, password);
        return { success: true, method: 'login', data: loginResult };
    } catch (loginError) {
        return { success: false, method: 'login', error: loginError };
    }
}

export const executeRefreshFlow = async () => {
    try {
        const refreshResult = await authApi.refresh();
        return { success: true, method: 'refresh', data: refreshResult };
    } catch (refreshError) {
        return { success: false, method: 'refresh', error: refreshError };
    }
}

export const executeRegisterFlow = async (username, password) => {
    try {
        const registerResult = await authApi.register(username, password);
        return { success: true, method: 'register', data: registerResult };
    } catch (registerError) {
        return { success: false, method: 'register', error: registerError };
    }
}