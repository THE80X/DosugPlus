import {executeListEventsFlow, executeCreateEventFlow} from "./services/event.js";
import {executeRefreshFlow} from "./services/auth.js"

let currentMode = 'events';
let currentOffset = 0;
let isLoading = false;
let hasMore = true;

// Форматирование даты
function formatDate(date) {
    return new Date(date).toLocaleString("ru-RU", {
        day: "2-digit",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

// Форматирование даты для бэкенда
function formatToBackend(datetimeLocal) {
    const d = new Date(datetimeLocal);
    const pad = n => String(n).padStart(2, "0");
    return `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// Рендер карточки события
function eventCard(event) {
    return `
        <div class="event-card" onclick="window.location.href='/main/event/${event.id}'">
            <div class="event-name">${event.name}</div>
            <div class="event-info">
                <div><strong>Организатор:</strong> ${event.owner_username}</div>
                <div><strong>Начало:</strong> ${formatDate(event.starts_at)}</div>
            </div>
            <span class="price ${event.price === 0 ? "free" : ""}">
                ${event.price === 0 ? "Бесплатно" : `Цена: ${event.price} ₽`}
            </span>
        </div>
    `;
}

// Загрузка событий
async function loadEvents(reset = true) {
    const content = document.getElementById('content');
    
    if (reset) {
        currentOffset = 0;
        hasMore = true;
        content.innerHTML = '<h1 class="page-title">Ближайшие мероприятия</h1><div class="loader">Загрузка...</div>';
    }

    if (!hasMore || isLoading) return;

    isLoading = true;

    const result = await executeListEventsFlow("for_user", 10, currentOffset);
    
    if (!result.success) {
        if (reset) {
            content.innerHTML = '<h1 class="page-title">Ближайшие мероприятия</h1><div style="color:red;">Ошибка загрузки</div>';
        }
        isLoading = false;
        return;
    }
    
    const events = result.data;
    
    if (events.length === 0) {
        hasMore = false;
        if (!reset) {
            content.insertAdjacentHTML('beforeend', '<div class="no-more-events"><p>📭 Больше нет мероприятий</p></div>');
        }
    } else {
        if (reset) {
            content.innerHTML = `<h1 class="page-title">Ближайшие мероприятия</h1><div class="events-grid">${events.map(eventCard).join("")}</div>`;
        } else {
            const eventsGrid = content.querySelector('.events-grid');
            if (eventsGrid) {
                eventsGrid.insertAdjacentHTML('beforeend', events.map(eventCard).join(""));
            }
        }
        currentOffset += events.length;
    }
    
    isLoading = false;
}

// Загрузка созданных событий
async function loadCreatedEvents(reset = true) {
    const content = document.getElementById('content');
    
    if (reset) {
        currentOffset = 0;
        hasMore = true;
        content.innerHTML = '<h1 class="page-title">Созданные мероприятия</h1><div class="loader">Загрузка...</div>';
    }

    if (!hasMore || isLoading) return;

    isLoading = true;

    const result = await executeListEventsFlow("created", 10, currentOffset);
    
    if (!result.success) {
        if (reset) {
            content.innerHTML = '<h1 class="page-title">Созданные мероприятия</h1><div style="color:red;">Ошибка загрузки</div>';
        }
        isLoading = false;
        return;
    }
    
    const events = result.data;
    
    if (events.length === 0) {
        hasMore = false;
        if (!reset) {
            content.insertAdjacentHTML('beforeend', '<div class="no-more-events"><p>📭 Больше нет мероприятий</p></div>');
        }
    } else {
        if (reset) {
            const modalHTML = `
                <button class="create-btn" id="openCreateModal">+ Создать мероприятие</button>
                <div class="modal" id="modal">
                    <div class="modal-content">
                        <h2>Создать мероприятие</h2>
                        <form id="createForm" class="form-grid">
                            <input name="name" placeholder="Название" required />
                            <input name="max_users_amount" type="number" placeholder="Макс. участников" required />
                            <textarea name="description" placeholder="Описание" required></textarea>
                            <input name="starts_at" type="datetime-local" required />
                            <input name="ends_at" type="datetime-local" required />
                            <input name="price" type="number" placeholder="Цена" required />
                            <div class="modal-actions">
                                <button type="submit">Создать</button>
                                <button type="button" id="closeModal">Отмена</button>
                            </div>
                        </form>
                    </div>
                </div>
            `;
            content.innerHTML = `<h1 class="page-title">Созданные мероприятия</h1>${modalHTML}<div class="events-grid">${events.map(eventCard).join("")}</div>`;
            
            // Навешиваем обработчики
            const openBtn = document.getElementById('openCreateModal');
            const closeBtn = document.getElementById('closeModal');
            const form = document.getElementById('createForm');
            
            if (openBtn) openBtn.onclick = openModal;
            if (closeBtn) closeBtn.onclick = closeModal;
            if (form) form.onsubmit = handleCreateEvent;
        } else {
            const eventsGrid = content.querySelector('.events-grid');
            if (eventsGrid) {
                eventsGrid.insertAdjacentHTML('beforeend', events.map(eventCard).join(""));
            }
        }
        currentOffset += events.length;
    }
    
    isLoading = false;
}

async function loadSignedEvents(reset = true) {

    const content = document.getElementById('content');

    if (reset) {
        currentOffset = 0;
        hasMore = true;

        content.innerHTML = `
            <h1 class="page-title">
                Мои записи
            </h1>

            <div class="loader">
                Загрузка...
            </div>
        `;
    }

    if (!hasMore || isLoading) return;

    isLoading = true;

    const result = await executeListEventsFlow(
        "signed",
        10,
        currentOffset
    );

    if (!result.success) {

        if (reset) {
            content.innerHTML = `
                <h1 class="page-title">
                    Мои записи
                </h1>

                <div style="color:red;">
                    Ошибка загрузки
                </div>
            `;
        }

        isLoading = false;
        return;
    }

    const events = result.data;

    if (events.length === 0) {

        hasMore = false;

        if (reset) {

            content.innerHTML = `
                <h1 class="page-title">
                    Мои записи
                </h1>

                <div class="empty-state">
                    Вы пока никуда не записаны
                </div>
            `;
        }

    } else {

        if (reset) {

            content.innerHTML = `
                <h1 class="page-title">
                    Мои записи
                </h1>

                <div class="events-grid">
                    ${events.map(eventCard).join("")}
                </div>
            `;

        } else {

            const eventsGrid =
                content.querySelector('.events-grid');

            if (eventsGrid) {

                eventsGrid.insertAdjacentHTML(
                    'beforeend',
                    events.map(eventCard).join("")
                );
            }
        }

        currentOffset += events.length;
    }

    isLoading = false;
}

// Обработка создания события
async function handleCreateEvent(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Валидация
    const maxUsers = parseInt(form.max_users_amount.value);
    const price = parseInt(form.price.value);
    const startsAt = form.starts_at.value;
    const endsAt = form.ends_at.value;
    
    if (maxUsers <= 0) {
        alert("Количество участников должно быть больше 0");
        return;
    }
    
    if (price < 0) {
        alert("Цена не может быть меньше 0");
        return;
    }
    
    const startsAtDate = new Date(startsAt);
    const endsAtDate = new Date(endsAt);
    
    if (endsAtDate <= startsAtDate) {
        alert("Дата окончания должна быть позже даты начала");
        return;
    }
    
    const payload = {
        name: form.name.value,
        max_users_amount: maxUsers,
        description: form.description.value,
        starts_at: formatToBackend(startsAt),
        ends_at: formatToBackend(endsAt),
        price: price
    };
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Создание...';
    
    const result = await executeCreateEventFlow(payload);
    
    if (!result.success) {
        alert(result.error.message || "Ошибка при создании мероприятия");
    } else {
        closeModal();
        form.reset();
        await loadCreatedEvents(true);
    }
    
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
}

// Модальные окна
function openModal() {
    const modal = document.getElementById('modal');
    if (modal) modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) modal.style.display = 'none';
}

// Обработка скролла
function handleScroll() {
    if (isLoading || !hasMore) return;
    
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    
    if (scrollTop + windowHeight >= documentHeight - 200) {
        if (currentMode === 'events') {
            loadEvents(false);
        } else if (currentMode === 'create') {
            loadCreatedEvents(false);
        }
    }
}

// Переключение табов
async function switchTab(mode) {
    const hasValidSession = await executeRefreshFlow();
    if (!hasValidSession.success){
        window.location.href = "/";
    }
    currentMode = mode;
    
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`.tab[data-page="${mode}"]`)?.classList.add('active');
    
    window.removeEventListener('scroll', handleScroll);
    
    const content = document.getElementById('content');
    
    switch(mode) {
        case 'events':
            await loadEvents(true);
            window.addEventListener('scroll', handleScroll);
            break;
        case 'create':
            await loadCreatedEvents(true);
            window.addEventListener('scroll', handleScroll);
            break;
        case 'my-tickets':
            await loadSignedEvents(true);
            window.addEventListener('scroll', handleScroll);
            // content.innerHTML = '<h1 class="page-title">Мои Записи</h1><p style="padding:40px;">Билеты...</p>';
            break;
        case 'profile':
            content.innerHTML = '<h1 class="page-title">Профиль</h1><p style="padding:40px;">Профиль...</p>';
            break;
    }
}

// Инициализация
async function init() {
    const hasValidSession = await executeRefreshFlow();
    if (!hasValidSession.success){
        window.location.href = "/";
    }
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const page = tab.dataset.page;
            if (page !== currentMode) {
                switchTab(page);
            }
        });
    });
    
    await switchTab('events');
}

document.addEventListener('DOMContentLoaded', init);