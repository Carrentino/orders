from helpers.errors import BaseError


class AlreadyAcceptedOrdersForThisPeriodError(BaseError):
    message = 'already accepted orders for this time period'


class CarsServiceError(BaseError):
    message = 'External service is unavailable'


class OrderRentPeriodDegreeOneHourError(BaseError):
    message = 'Rent period is degree then 1 hour'
