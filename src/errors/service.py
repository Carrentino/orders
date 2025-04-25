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


class UserServiceIsUnavailableError(BaseError):
    message = 'User service is unavailable'


class NotOwnerOfContractError(BaseError):
    message = 'You are not owner of this contract'


class NotFoundContractError(BaseError):
    message = 'Not found this contract'


class InvalidOrExpiredCodeError(BaseError):
    message = 'Code has expired or invalid'


class NotRenterOrLessorOrderError(BaseError):
    message = 'You must be lessor or renter of order'


class OrderStatusMustBeAcceptedError(BaseError):
    message = 'Order status must be accepted'


class OrderStatusMustBeInProgressError(BaseError):
    message = 'Order status must be in progress'
