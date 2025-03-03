import enum


class OrderStatus(enum.Enum):
    UNDER_CONSIDERATION = 0  # На рассмотрении
    ACCEPTED = 1  # Подтвержден
    REJECTED = 2  # Отклонен
    CANCELED = 3  # Отменен
    IN_PROGRESS = 4  # Выполняется
    FINISHED = 5  # Завершен
