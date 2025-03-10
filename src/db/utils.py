from src.db.consts import OrderStatus


def get_higher_statuses(current_status: OrderStatus) -> list[OrderStatus]:
    all_statuses = list(OrderStatus)
    current_index = all_statuses.index(current_status)
    return all_statuses[current_index + 1 :]
