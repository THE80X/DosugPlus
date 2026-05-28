import { api } from "./api_requests.js";
import { executeEventFlow, executeEventUserStatusFlow, executeMyEventUserStatusFlow, executeEventUserFlow, executeEventUserListFlow} from "./services/event.js";


async function get_event(event_id) {
    const eventResult = await executeEventFlow(event_id);
    if (eventResult.success){
        return eventResult.data;
    }else{
        if (eventResult.error.status === 400 && eventResult.error.message === "EVENT_NOT_EXIST") {
            throw new Error("Мероприятие не существует");
        }
        throw new Error(eventResult.error.message || "Ошибка при загрузке мероприятия");
    }
}


async function get_event_users(event_id, flag, limit, offset) {
    const eventUserResult = await executeEventUserListFlow(event_id, flag, limit, offset);
    if (eventUserResult.success){
        return eventUserResult.data;
    }else{
        if (eventUserResult.error.status === 400 && eventUserResult.error.message === "USER_IS_NOT_OWNER") {
            throw new Error("Пользователь не является организатором Мероприятия");
        }
        if (eventUserResult.error.status === 400 && eventUserResult.error.message === "EVENT_NOT_EXIST") {
            throw new Error("Мероприятие не существует");
        }
        throw new Error(eventUserResult.error.message || "Ошибка при загрузке списка пользователей");
    }
}


async function get_event_user_status(event_id) {
    const userResult = await executeEventUserFlow(event_id);
    if (userResult.success){
        return userResult.data;
    }else{
        if (userResult.error.status === 400 && userResult.error.message === "EVENT_NOT_EXIST") {
            throw new Error("Мероприятие не существует");
        }
        throw new Error(userResult.error.message || "Ошибка при загрузке статуса пользователя");
    }
}


async function post_event_user_status(event_id, status, username) {
    const statusResult = await executeEventUserStatusFlow(event_id, status, username);
    if (statusResult.success){
        return statusResult.data;
    }else{
        if (statusResult.error.status === 400 && statusResult.error.message === "EVENT_NOT_EXIST") {
            throw new Error("Мероприятие не существует");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "USER_NOT_EXIST") {
            throw new Error("Пользователь не существует");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "UNKNOWN_STATUS") {
            throw new Error("Неизвестный статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "WRONG_STATUS") {
            throw new Error("Неправильный статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "EVENT_FULL") {
            throw new Error("Мероприятие уже заполнено");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "USER_IS_OWNER") {
            throw new Error("Организатор не может изменить свой статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "NOT_USER_OR_OWNER") {
            throw new Error("Пользователь не является ни участником, ни организатором мероприятия");
        }
        throw new Error(statusResult.error.message || "Ошибка при изменении статуса пользователя");
    }
}


async function post_my_event_user_status(event_id, status) {
    const statusResult = await executeMyEventUserStatusFlow(event_id, status);
    if (statusResult.success){
        return statusResult.data;
    }else{
        if (statusResult.error.status === 400 && statusResult.error.message === "EVENT_NOT_EXIST") {
            throw new Error("Мероприятие не существует");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "USER_NOT_EXIST") {
            throw new Error("Пользователь не существует");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "UNKNOWN_STATUS") {
            throw new Error("Неизвестный статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "WRONG_STATUS") {
            throw new Error("Неправильный статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "EVENT_FULL") {
            throw new Error("Мероприятие уже заполнено");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "USER_IS_OWNER") {
            throw new Error("Организатор не может изменить свой статус");
        }
        if (statusResult.error.status === 400 && statusResult.error.message === "NOT_USER_OR_OWNER") {
            throw new Error("Пользователь не является ни участником, ни организатором мероприятия");
        }
        throw new Error(statusResult.error.message || "Ошибка при изменении статуса пользователя");
    }
}


function renderEvent(event) {
    const container = document.getElementById("event-content");

    container.innerHTML = `
        ${
            event.user_is_owner
                ? `
                <div class="tabs-header">
                    <div class="tab active" data-tab="event-info">
                        Информация
                    </div>

                    <div class="tab" data-tab="users">
                        Пользователи
                    </div>
                </div>
            `
                : ""
        }

        <div class="content">
            <div class="tab-content active" id="event-info">

                <h1 class="page-title">${event.name}</h1>

                <div class="event-detail">

                    <div class="event-detail-grid">
                        <div>
                            <b>Организатор:</b><br>
                            ${event.owner_username}
                        </div>

                        <div>
                            <b>Цена:</b><br>
                            ${event.price ? event.price + " ₽" : "Бесплатно"}
                        </div>

                        <div>
                            <b>Начало:</b><br>
                            ${event.starts_at}
                        </div>

                        <div>
                            <b>Конец:</b><br>
                            ${event.ends_at}
                        </div>

                        <div>
                            <b>Участники:</b><br>
                            ${event.total_users_amount} / ${event.max_users_amount}
                        </div>
                    </div>

                    <div class="event-description">
                        <h3>Описание</h3>
                        <p>${event.description}</p>
                    </div>

                    ${
                        !event.user_is_owner
                            ? `<div id="event-actions"></div>`
                            : ""
                    }

                </div>
            </div>

            ${
                event.user_is_owner
                    ? `
                    <div class="tab-content" id="users">
                        <div class="loader">
                            Загрузка пользователей...
                        </div>
                    </div>
                `
                    : ""
            }
        </div>
    `;
}


function setupTabs(eventId) {
    const tabs = document.querySelectorAll(".tab");

    tabs.forEach((tab) => {
        tab.addEventListener("click", async () => {

            document.querySelectorAll(".tab").forEach((t) => {
                t.classList.remove("active");
            });

            document.querySelectorAll(".tab-content").forEach((c) => {
                c.classList.remove("active");
            });

            tab.classList.add("active");

            const tabName = tab.dataset.tab;

            const currentTab = document.getElementById(tabName);

            currentTab.classList.add("active");

            // Загрузка пользователей
            if (tabName === "users") {
                await loadUsersTab(eventId);
            }
        });
    });
}


async function loadUsersTab(eventId) {
    const usersContainer = document.getElementById("users");

    usersContainer.innerHTML = `
        <div class="loader">
            Загрузка...
        </div>
    `;

    try {
        const users = await get_event_users(eventId, "signed", 10, 0);

        if (!users || users.length === 0) {
            usersContainer.innerHTML = `
                <div class="empty-state">
                    Пользователей нет
                </div>
            `;
            return;
        }

        usersContainer.innerHTML = `
            <div class="users-list">
                ${users.map(user => `
                    <div class="user-item">

                        <div>
                            <b>${user.username}</b>
                            <br>
                            Статус: ${user.status}
                        </div>

                        <button
                            class="kick-btn"
                            data-username="${user.username}"
                        >
                            Исключить
                        </button>

                    </div>
                `).join("")}
            </div>
        `;

        const kickButtons =
            usersContainer.querySelectorAll(".kick-btn");

        kickButtons.forEach((btn) => {
            btn.addEventListener("click", async () => {

                const username = btn.dataset.username;

                try {
                    await post_event_user_status(
                        eventId,
                        "kicked",
                        username
                    );

                    btn.closest(".user-item").remove();

                } catch (err) {
                    alert(err.message);
                }
            });
        });

    } catch (err) {
        usersContainer.innerHTML = `
            <div class="empty-state">
                ${err.message}
            </div>
        `;
    }
}


async function setupOwnerPanel(eventId) {
    const usersBtn = document.getElementById("show-users-btn");

    if (!usersBtn) return;

    usersBtn.addEventListener("click", async () => {
        const usersContainer = document.getElementById("users-container");

        usersContainer.innerHTML = `<div class="loader">Загрузка...</div>`;

        try {
            const users = await get_event_users(eventId, "signed");

            if (!users || users.length === 0) {
                usersContainer.innerHTML = `
                    <div class="empty-state">
                        Пользователей нет
                    </div>
                `;
                return;
            }

            usersContainer.innerHTML = `
                <div class="users-list">
                    ${users
                        .map(
                            (user) => `
                                <div class="user-item">
                                    <div>
                                        <b>${user.username}</b>
                                        <br>
                                        Статус: ${user.status}
                                    </div>

                                    <button 
                                        class="kick-btn"
                                        data-username="${user.username}"
                                    >
                                        Исключить
                                    </button>
                                </div>
                            `
                        )
                        .join("")}
                </div>
            `;

            const kickButtons =
                usersContainer.querySelectorAll(".kick-btn");

            kickButtons.forEach((btn) => {
                btn.addEventListener("click", async () => {
                    const username = btn.dataset.username;

                    try {
                        await post_event_user_status(
                            eventId,
                            "kicked",
                            username
                        );

                        btn.closest(".user-item").remove();

                    } catch (err) {
                        alert(err.message);
                    }
                });
            });

        } catch (err) {
            usersContainer.innerHTML = `
                <div class="empty-state">
                    ${err.message}
                </div>
            `;
        }
    });
}


async function setupUserButton(eventId) {
    const actionsContainer = document.getElementById("event-actions");

    try {
        const statusData = await get_event_user_status(eventId);

        const needJoinButton =
            statusData === null ||
            statusData === "left" ||
            statusData === "kicked";

        if (needJoinButton) {
            actionsContainer.innerHTML = `
                <button class="join-btn" id="action-btn">
                    Записаться
                </button>
            `;

            document
                .getElementById("action-btn")
                .addEventListener("click", async () => {
                    try {
                        await post_my_event_user_status(eventId, "signed");

                        actionsContainer.innerHTML = `
                            <button class="join-btn" id="leave-btn">
                                Покинуть
                            </button>
                        `;

                        setupLeaveButton(eventId);

                    } catch (err) {
                        alert(err.message);
                    }
                });

            return;
        }

        if (statusData === "signed") {
            actionsContainer.innerHTML = `
                <button class="join-btn" id="leave-btn">
                    Покинуть
                </button>
            `;

            setupLeaveButton(eventId);
        }

    } catch (err) {
        actionsContainer.innerHTML = `
            <div class="empty-state">
                ${err.message}
            </div>
        `;
    }
}


function setupLeaveButton(eventId) {
    const leaveBtn = document.getElementById("leave-btn");

    if (!leaveBtn) return;

    leaveBtn.addEventListener("click", async () => {
        try {
            await post_my_event_user_status(eventId, "left");

            const actionsContainer =
                document.getElementById("event-actions");

            actionsContainer.innerHTML = `
                <button class="join-btn" id="join-btn">
                    Записаться
                </button>
            `;

            setupUserButton(eventId);

        } catch (err) {
            alert(err.message);
        }
    });
}


async function loadEvent() {
    const container = document.getElementById("event-content");

    const pathParts = window.location.pathname.split("/");
    const eventId = pathParts[pathParts.length - 1];

    try {
        const event = await get_event(eventId);

        renderEvent(event);

        if (event.user_is_owner) {
            setupTabs(eventId);
        } else {
            await setupUserButton(eventId);
        }

    } catch (err) {
        container.innerHTML = `
            <div class="empty-state">
                ${err.message}
            </div>
        `;

        console.error(err);
    }
}


window.addEventListener("DOMContentLoaded", loadEvent);