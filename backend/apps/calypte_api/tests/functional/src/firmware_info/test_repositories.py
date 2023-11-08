import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.firmware.models import FirmwareInfo
from calypte_api.firmware.repositories import FirmwareInfoRepo
from calypte_api.types.models import Type
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def firm_info_repo(db_session: AsyncSession):
    return FirmwareInfoRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_firm_info_data(
    db_session: AsyncSession,
):
    company_ids = [uuid4() for _ in range(2)]
    type_values = [
        {
            "id": uuid4(),
            "company_id": random.choice(company_ids),
            "name": f"test name {i}",
            "description": f"test description {i}",
            "created_at": datetime.now(),
        }
        for i in range(10)
    ]
    await db_session.execute(insert(Type).values(type_values))

    firmware_values = []
    for i in range(100):
        type_obj = random.choice(type_values)
        firmware_values.append(
            {
                "id": uuid4(),
                "company_id": type_obj["company_id"],
                "type_id": type_obj["id"],
                "name": f"test name {i}",
                "serial_number": f"test serial number {i}",
                "description": f"test firmware description {i}",
                "version": "v1.0.0",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(FirmwareInfo).values(firmware_values))

    await db_session.commit()
    return firmware_values


async def test_get_firm_info_by_id(
    test_firm_info_data: list[dict],
    firm_info_repo: FirmwareInfoRepo,
) -> None:
    exp_firm_info = test_firm_info_data[0]
    firm_info_object = await firm_info_repo.get_firmware_by_id(
        company_id=exp_firm_info["company_id"],
        firmware_id=exp_firm_info["id"],
    )
    assert firm_info_object.id == exp_firm_info["id"]
    assert firm_info_object.name == exp_firm_info["name"]
    assert firm_info_object.description == exp_firm_info["description"]
    assert firm_info_object.company_id == exp_firm_info["company_id"]
    assert firm_info_object.type_id == exp_firm_info["type_id"]


@pytest.mark.parametrize(
    "firm_info",
    [
        {
            "name": "test name",
            "description": "test description",
            "serial_number": "test serial number",
            "version": "v1.0.0",
            "company_id": uuid4(),
        }
    ],
)
async def test_create_firm_info(
    firm_info_repo: FirmwareInfoRepo,
    test_firm_info_data: list[dict],
    firm_info: dict,
) -> None:
    expected_firm_info = test_firm_info_data[0]

    new_firm_info = {
        **firm_info,
        "type_id": expected_firm_info["type_id"],
    }

    firm_info_object = await firm_info_repo.create_firmware(**new_firm_info)
    assert firm_info_object.name == firm_info["name"]
    assert firm_info_object.description == firm_info["description"]
    assert firm_info_object.company_id == firm_info["company_id"]


@pytest.mark.parametrize(
    "firm_info",
    [
        {
            "name": "test name",
            "description": "test description",
            "serial_number": "test serial number",
            "version": "v1.0.0",
        }
    ],
)
async def test_update_firm_info(
    test_firm_info_data: list[dict],
    firm_info_repo: FirmwareInfoRepo,
    firm_info: dict,
) -> None:
    expected_firm_info = test_firm_info_data[0]

    new_firm_info = {
        **firm_info,
        "company_id": expected_firm_info["company_id"],  # type: ignore
        "firmware_id": expected_firm_info["id"],
    }

    firm_info_object = await firm_info_repo.update_firmware(**new_firm_info)

    assert firm_info_object.name == new_firm_info["name"]
    assert firm_info_object.description == new_firm_info["description"]
    assert firm_info_object.version == new_firm_info["version"]
    assert firm_info_object.id == new_firm_info["firmware_id"]


async def test_check_firm_info_belongs_to(
    test_firm_info_data: list[dict],
    firm_info_repo: FirmwareInfoRepo,
) -> None:
    expected_firm_info = test_firm_info_data[0]

    assert await firm_info_repo.check_firmware_belongs_to(
        firmware_id=expected_firm_info["id"],
        company_id=expected_firm_info["company_id"],
    )


async def test_check_firm_info_does_not_belong_to(
    test_firm_info_data: list[dict],
    firm_info_repo: FirmwareInfoRepo,
) -> None:
    expected_firm_info = test_firm_info_data[0]

    assert not await firm_info_repo.check_firmware_belongs_to(
        firmware_id=expected_firm_info["id"],
        company_id=uuid4(),
    )
