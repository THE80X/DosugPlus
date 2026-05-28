import { api } from "./requests.js";

export const userApi = {
    postUserBlacklist: (username) => {
        return api.post(`/v1/user/blacklist`, { username: username });
    },
    deleteUserBlacklist: (username) => {
        return api.delete(`/v1/user/blacklist`, { username: username });
    }
};