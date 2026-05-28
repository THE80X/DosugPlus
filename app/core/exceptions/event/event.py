from app.schemas.enum import ErrorCode


ERROR_DETAILS = {
    ErrorCode.MAX_USERS_NEGATIVE: {
        "message": "Количество участников должно быть больше 0"
    },
    ErrorCode.PRICE_NEGATIVE: {
        "message": "Цена не может быть отрицательной"
    },
    ErrorCode.USER_ALREDY_EXISTS:{
        "message": "Такой пользователь уже существует"
    },
    ErrorCode.WRONG_DATETIME_FORMAT:{
        "message": "Не подходящий формат даты и времени"
    },
    ErrorCode.END_BEFORE_START_OR_EQUAL:{
        "message": "Дата начала мероприятия не может быть той же, что и у даты завершения или быть позже"
    }
}