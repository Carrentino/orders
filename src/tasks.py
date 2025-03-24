import datetime
import uuid
from io import BytesIO
from pathlib import Path
from uuid import UUID

from helpers.depends.db_session import get_db_session_context
from jinja2 import Environment, FileSystemLoader, select_autoescape
from asgiref.sync import async_to_sync
from weasyprint import HTML

from src.celery_conf import celery_app
from src.db.models.contract import Contract
from src.db_client import make_db_client
from src.integrations.cars import CarsClient
from src.integrations.notifications import NotificationsKafkaProducer
from src.repositories.order import OrderRepository
from src.settings import get_settings
from src.web.depends.integrations import get_users_client
from src.web.depends.service import get_order_service


@celery_app.task
def generate_contract(order_id: str):
    async_to_sync(async_generate_contract)(order_id)


async def async_generate_contract(order_id: str):
    async with get_db_session_context(make_db_client()) as session:
        order_service = await get_order_service(
            OrderRepository(session=session), CarsClient(), NotificationsKafkaProducer()
        )
        order = await order_service.order_repository.get(UUID(order_id))
        env = Environment(loader=FileSystemLoader('src/static'), autoescape=select_autoescape(["html"]))
        template = env.get_template('contract_template.html')
        users_client = await get_users_client()
        renter_data_resp = await users_client.get_user_info(str(order.renter_id))
        lessor_data_resp = await users_client.get_user_info(str(order.lessor_id))
        renter_data = renter_data_resp.json()[0]
        lessor_data = lessor_data_resp.json()[0]
        logo_path = Path('src/static') / "logo.jpg"
        contract_data = {
            "contract_number": order.id,
            'logo_path': logo_path,
            "contract_date": datetime.datetime.now(),
            "customer_name": ' '.join([renter_data.get('last_name'), renter_data.get('first_name')]),
            "executor_name": ' '.join([lessor_data.get('last_name'), lessor_data.get('first_name')]),
            "total_amount": str(order.total_price),
            "contract_terms": "Условия договора...",
        }

        html_content = template.render(contract_data)
        storage = get_settings().storage
        pdf_bytes = HTML(string=html_content).write_pdf()
        file = BytesIO(pdf_bytes)
        filename = f"contracts/{order.id}/{uuid.uuid4().hex}.pdf"
        storage.write(file, filename)
        contract = Contract(
            filename=filename,
            order=order,
        )

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        order.contract_id = contract.id
        await session.commit()
