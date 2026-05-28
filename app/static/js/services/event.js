import { api } from "./requests.js";

export const eventApi = {
    createEvent: (payload) => {
        return api.post(`/v1/events`, payload);
    },
    getEventList: (flag, limit, offset) => {
        return api.get(`/v1/events?event_flag=${flag}&limit=${limit}&offset=${offset}`);
    },
    getEvent: (eventId) => {
        return api.get(`/v1/events/${eventId}`);
    },
    
    getEventUserList: (eventId, flag=null, limit, offset) => {
        let url = `/v1/events/${eventId}/users?limit=${limit}&offset=${offset}`;
        if (flag !== null) {
            url += `&status=${flag}`;
        }
        return api.get(url);
    },

    getMyEventUserStatus: (eventId) => {
        return api.get(`/v1/events/${eventId}/users/me`);
    },
    postMyEventUserStatus: (eventId, status, username) => {
        return api.post(`/v1/events/${eventId}/users/me`, { status: status});
    },
    postEventUserStatus: (eventId, status, username) => {
        return api.post(`/v1/events/${eventId}/users/${username}`, { status: status});
    },
};


export async function executeMyEventUserStatusFlow(eventId, status, username) {
    try {
        const statusResult = await eventApi.postMyEventUserStatus(eventId, status, username);
        return { success: true, method: "postMyEventUserStatus", data: statusResult };
    } catch (error) {
        return { success: false, method: "postMyEventUserStatus", error: error };
    }
}


// Поток загрузки события
export async function executeEventFlow(eventId) {
    try {
        const eventResult = await eventApi.getEvent(eventId);
        return { success: true, method: "getEvent", data: eventResult };
    } catch (error) {
        return { success: false, method: "getEvent", error: error };
    }
}

// Поток загрузки событий
export async function executeListEventsFlow(flag, limit, offset) {
    try {
        const getEventsResult = await eventApi.getEventList(flag, limit, offset);
        return { success: true, method: "getEventList", data: getEventsResult };
    } catch (error) {
        return { success: false, method: "getEventList", error: error };
    }
}

// Поток создания события
export async function executeCreateEventFlow(payload) {
    try {
        const createResult = await eventApi.createEvent(payload);
        return { success: true, method: "createEvent", data: createResult };
    } catch (error) {
        return { success: false, method: "createEvent", error: error };
    }
}

// Поток изменения статуса пользователя в событии
export async function executeEventUserStatusFlow(eventId, status, username) {
    try {
        const statusResult = await eventApi.postEventUserStatus(eventId, status, username);
        return { success: true, method: "postEventUserStatus", data: statusResult };
    } catch (error) {
        return { success: false, method: "postEventUserStatus", error: error };
    }
}

// Поток загрузки списка пользователей события
export async function executeEventUserListFlow(eventId, flag, limit, offset) {
    try {
        const listResult = await eventApi.getEventUserList(eventId, flag, limit, offset);
        return { success: true, method: "getEventUserList", data: listResult };
    } catch (error) {
        return { success: false, method: "getEventUserList", error: error };
    }
}

// Поток загрузки статуса обратившегося пользователя в событии
export async function executeEventUserFlow(eventId) {
    try {
        const userResult = await eventApi.getMyEventUserStatus(eventId);
        return { success: true, method: "getMyEventUserStatus", data: userResult };
    } catch (error) {
        return { success: false, method: "getMyEventUserStatus", error: error };
    }
}