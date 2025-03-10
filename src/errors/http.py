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
