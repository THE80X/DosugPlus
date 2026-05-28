function httpRequest(method, url, data = null, isFormData = false) {
    return new Promise(function (resolve, reject) {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.withCredentials = true; // ВАЖНО - РАСКОММЕНТИРОВАЛ
        
        // Устанавливаем Content-Type только если это НЕ FormData
        if (isFormData) {
            // ничего не ставим
        } else {
            xhr.setRequestHeader("Content-Type", "application/json");
        }

        const accessToken = getCookie('access_token');
        const refreshToken = getCookie('refresh_token');
        if (accessToken) {
            xhr.setRequestHeader("Authorization", `Bearer ${accessToken}`);
        }
        if (refreshToken) {
            xhr.setRequestHeader("Refresh", refreshToken);
        }
        
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        resolve(JSON.parse(xhr.responseText));
                    } catch {
                        resolve(xhr.responseText);
                    }
                } else {
                    // Парсим ошибку из ответа
                    let errorDetail = null;
                    let errorResponse = null;
                    
                    try {
                        const errorData = JSON.parse(xhr.responseText);
                        errorDetail = errorData.detail;
                        errorResponse = errorData;
                    } catch {
                        errorResponse = xhr.responseText;
                    }
                    
                    // Создаем объект ошибки с деталями
                    const error = new Error(errorDetail || xhr.statusText || `Ошибка ${xhr.status}`);
                    error.status = xhr.status;
                    error.statusText = xhr.statusText;
                    error.detail = errorDetail;
                    error.response = errorResponse;
                    
                    reject(error);
                }
            }
        };

        xhr.onerror = function () {
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            });
        };

        // Отправляем данные в зависимости от типа
        if (isFormData) {
            xhr.send(data); // FormData отправляем как есть
        } else {
            xhr.send(data ? JSON.stringify(data) : null); // JSON данные
        }
    });
}

export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Функция для зачистки кук
export function clearAuthCookies() {
    const cookies = ['access_token', 'refresh_token'];
    cookies.forEach(cookieName => {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    });
}

// Удобные обёртки
export const api = {
    get: (url) => httpRequest("GET", url),
    post: (url, data, isFormData = false) => httpRequest("POST", url, data, isFormData),
    put: (url, data, isFormData = false) => httpRequest("PUT", url, data, isFormData),
    delete: (url) => httpRequest("DELETE", url)
};