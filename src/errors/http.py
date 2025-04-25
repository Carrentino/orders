from helpers.errors import ServerError
from starlette import status


class AlreadyAcceptedOrdersForThisPeriodHttpError(ServerError):
    message = 'Already accepted orders for this time period'
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
    message = 'For change order status to accepted current status of order must be under consideration'
    status_code = status.HTTP_403_FORBIDDEN


class OrderNotFoundHttpError(ServerError):
    message = 'Not Found this order'
    status_code = status.HTTP_404_NOT_FOUND


class NotOwnerOfContractHttpError(ServerError):
    message = 'You are not owner of this contract'
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundContractHttpError(ServerError):
    message = 'Not found this contract'
    status_code = status.HTTP_404_NOT_FOUND


class InvalidOrExpiredCodeHttpError(ServerError):
    message = 'Code has expired or invalid'
    status_code = status.HTTP_400_BAD_REQUEST
