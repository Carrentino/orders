import enum


class OrderStatus(enum.StrEnum):
    UNDER_CONSIDERATION = 'На рассмотрении'
    ACCEPTED = 'Подтвержден'
    REJECTED = 'Отклонен'
    CANCELED = 'Отменен'
    IN_PROGRESS = 'Выполняется'
    FINISHED = 'Завершен'
