const createHeaders = (isFormData = false) => {
    const headers = {};
    if (!isFormData) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
};

const parseResponse = async (response) => {
    const text = await response.text();
    try {
        return JSON.parse(text);
    } catch {
        return text;
    }
};

const handleResponse = async (response) => {
    const data = await parseResponse(response);
    
    if (!response.ok) {
        const error = new Error(data?.message || data?.detail || response.statusText);
        error.status = response.status;
        error.data = data;
        throw error;
    }
    
    return data;
};

const httpRequest = (method, url, data = null, options = {}) => {
    const { isFormData = false, withCredentials = true } = options;
    
    const headers = {};
    if (!isFormData) {
        headers['Content-Type'] = 'application/json';
    }
    
    return fetch(url, {
        method,
        headers,
        body: data ? (isFormData ? data : JSON.stringify(data)) : null,
        credentials: withCredentials ? 'include' : 'omit' // Ключевой момент!
    }).then(handleResponse);
};

export const api = {
    // Обычные запросы с куками
    get: (url, options) => httpRequest('GET', url, null, { ...options, withCredentials: true }),
    post: (url, data, options) => httpRequest('POST', url, data, { ...options, withCredentials: true }),
    put: (url, data, options) => httpRequest('PUT', url, data, { ...options, withCredentials: true }),
    delete: (url, options) => httpRequest('DELETE', url, null, { ...options, withCredentials: true }),

    // Запросы БЕЗ кук (для login)
    postWithoutCookies: (url, data, options) => httpRequest('POST', url, data, { ...options, withCredentials: false }),
};