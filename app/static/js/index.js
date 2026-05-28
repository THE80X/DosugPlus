import { authApi, executeLoginFlow, executeRefreshFlow, executeRegisterFlow } from "./services/auth.js";


// Регистрация + автоматический вход
async function register(username, password) {
    const registerResult = await executeRegisterFlow(username, password);

    if (registerResult.success){
        const loginResult = await executeLoginFlow(username, password);
        if (loginResult.success){
            window.location.href = "/main";
        }else{
            throw new Error(loginResult.error.message || "Ошибка при входе после регистрации");
        }
    }else{
        if (registerResult.error.status === 400 && registerResult.error.message === "USER_ALREDY_EXISTS") {
            throw new Error("Пользователь с таким именем уже существует");
        }
        throw new Error(registerResult.error.message || "Ошибка при регистрации");
    }
}

async function login(username, password) {
    const loginResult = await executeLoginFlow(username, password);
    if (loginResult.success){
        window.location.href = "/main";
    }else{
        throw new Error(loginResult.error.message || "Ошибка при входе");
    }
}

// Инициализация приложения
async function init() {
    const hasValidSession = await executeRefreshFlow();
    if (hasValidSession.success){
        window.location.href = "/main";
    }

    // Если сессия не валидна — показываем форму
    document.getElementById('loader').style.opacity = '0';
    setTimeout(() => {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('auth-screen').style.display = 'block';
    }, 400);

    let currentMode = 'login';

    const tabs = document.getElementById('tabs');
    const form = document.getElementById('auth-form');
    const submitBtn = document.getElementById('submit-btn');
    const errorEl = document.getElementById('error-message');
    const confirmGroup = document.getElementById('confirm-password-group');
    const confirmInput = document.getElementById('confirm-password');

    tabs.addEventListener('click', (e) => {
        if (!e.target.classList.contains('tab-btn')) return;

        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        e.target.classList.add('active');

        currentMode = e.target.dataset.mode;

        if (currentMode === 'register') {
            confirmGroup.style.display = 'block';
            confirmInput.required = true;
            submitBtn.textContent = 'Зарегистрироваться';
        } else {
            confirmGroup.style.display = 'none';
            confirmInput.required = false;
            submitBtn.textContent = 'Войти';
        }

        errorEl.textContent = '';
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = confirmInput.value;

        errorEl.textContent = '';

        if (!username || !password) {
            errorEl.textContent = 'Пожалуйста, заполните все поля';
            return;
        }

        if (currentMode === 'register') {
            if (password !== confirmPassword) {
                errorEl.textContent = 'Пароли не совпадают';
                return;
            }
            if (password.length < 6) {
                errorEl.textContent = 'Пароль должен содержать минимум 6 символов';
                return;
            }
        }

        submitBtn.disabled = true;
        submitBtn.textContent = currentMode === 'register' ? 'Регистрация...' : 'Вход...';

        try {
            if (currentMode === 'login') {
                await login(username, password);
            } else {
                await register(username, password);
            }
        } catch (err) {
            errorEl.textContent = err.message;
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = currentMode === 'register' ? 'Зарегистрироваться' : 'Войти';
        }
    });
}

window.addEventListener('DOMContentLoaded', init);