from helpers.errors import ServerError
from starlette import status


class AlreadyAcceptedOrdersForThisPeriodHttpError(ServerError):
    message = 'already accepted orders for this time period'
    status_code = status.HTTP_409_CONFLICT


class CarsServiceHttpError(ServerError):
    message = 'External service is unavailable'
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class OrderRentPeriodDegreeOneHourHttpError(ServerError):
    message = 'Rent period is degree then 1 hour'
    status_code = status.HTTP_403_FORBIDDEN


class NotLessorOrderHttpError(ServerError):
    message = 'User must be a lessor of order for change status of order to current'
    status_code = status.HTTP_403_FORBIDDEN


class NotRenterOrderHttpError(ServerError):
    message = 'User must be a renter of order for change status of order to current'
    status_code = status.HTTP_403_FORBIDDEN


class OrderStatusMustBeUnderConsiderationHttpError(ServerError):
    message = 'for change order status to accepted current status of order must be under consideration'
    status_code = status.HTTP_403_FORBIDDEN


class OrderNotFoundHttpError(ServerError):
    message = 'NotFound this order'
    status_code = status.HTTP_404_NOT_FOUND
