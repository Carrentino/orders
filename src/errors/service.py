from helpers.errors import BaseError


class AlreadyAcceptedOrdersForThisPeriodError(BaseError):
    message = 'Already accepted orders for this time period'


class CarsServiceError(BaseError):
    message = 'External service is unavailable'


class OrderRentPeriodDegreeOneHourError(BaseError):
    message = 'Rent period is degree then 1 hour'


class NotLessorOrderError(BaseError):
    message = 'User must be a lessor of order for change status of order to current'


class NotRenterOrderError(BaseError):
    message = 'User must be a renter of order for change status of order to current'


class OrderStatusMustBeUnderConsiderationError(BaseError):
    message = 'For change order status to accepted current status of order must be under consideration'


class OrderNotFoundError(BaseError):
    message = 'Not found this order'
