from src.integrations.cars import CarsClient


async def get_cars_client() -> CarsClient:
    return CarsClient()
