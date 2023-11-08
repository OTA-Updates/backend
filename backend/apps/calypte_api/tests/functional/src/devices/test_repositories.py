import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.devices.models import Device
from calypte_api.devices.repositories import DeviceRepo
from calypte_api.firmware.models import FirmwareInfo
from calypte_api.groups.models import Group
from calypte_api.types.models import Type
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def device_repo(db_session: AsyncSession):
    return DeviceRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_device_data(
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

    group_values = []
    for i in range(100):
        type_obj = random.choice(type_values)
        group_values.append(
            {
                "id": uuid4(),
                "company_id": type_obj["company_id"],
                "type_id": type_obj["id"],
                "name": f"test name {i}",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(Group).values(group_values))

    device_values = []
    for i in range(100):
        type_obj = random.choice(type_values)
        current_firmware = random.choice(firmware_values)
        assigned_firmware = random.choice(firmware_values)
        group = random.choice(group_values)
        device_values.append(
            {
                "id": uuid4(),
                "name": f"test name {i}",
                "description": f"test description {i}",
                "serial_number": f"serial number {i}",
                "company_id": type_obj["company_id"],
                "type_id": type_obj["id"],
                "current_firmware_id": current_firmware["id"],
                "assigned_firmware_id": assigned_firmware["id"],
                "group_id": group["id"],
                "registered_at": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(Device).values(device_values))

    await db_session.commit()
    return device_values


async def test_get_device_by_id(
    test_device_data: list[dict],
    device_repo: DeviceRepo,
) -> None:
    expected_device = test_device_data[0]
    device_object = await device_repo.get_device_by_id(
        company_id=expected_device["company_id"],
        device_id=expected_device["id"],
    )
    assert device_object is not None
    assert device_object.id == expected_device["id"]
    assert device_object.name == expected_device["name"]
    assert device_object.description == expected_device["description"]
    assert device_object.registered_at == expected_device["registered_at"]
    assert device_object.company_id == expected_device["company_id"]
    assert device_object.type_id == expected_device["type_id"]
    assert (
        device_object.current_firmware_id
        == expected_device["current_firmware_id"]
    )


@pytest.mark.parametrize(
    "device",
    [
        {
            "name": "test name",
            "description": "test description",
            "company_id": uuid4(),
            "serial_number": "serial number",
        }
    ],
)
async def test_create_device(
    device_repo: DeviceRepo,
    test_device_data: list[dict],
    device: dict,
) -> None:
    expected_device = test_device_data[0]

    new_device = {
        **device,
        "type_id": expected_device["type_id"],
        "group_id": expected_device["group_id"],
        "assigned_firmware_id": expected_device["assigned_firmware_id"],
    }

    device_object = await device_repo.create_device(**new_device)
    assert device_object.name == device["name"]
    assert device_object.description == device["description"]
    assert device_object.company_id == device["company_id"]


@pytest.mark.parametrize(
    "device",
    [
        {
            "name": "test name",
            "description": "test description",
            "serial_number": "serial number",
        }
    ],
)
async def test_update_device(
    test_device_data: list[dict],
    device_repo: DeviceRepo,
    device: dict,
) -> None:
    expected_device = test_device_data[0]

    new_device = {
        **device,
        "company_id": expected_device["company_id"],
        "device_id": expected_device["id"],
        "group_id": expected_device["group_id"],
        "assigned_firmware_id": expected_device["assigned_firmware_id"],
    }

    device_object = await device_repo.update_device(**new_device)

    assert device_object.name == new_device["name"]
    assert device_object.description == new_device["description"]
    assert device_object.id == new_device["device_id"]


async def test_delete_device(
    test_device_data: list[dict],
    device_repo: DeviceRepo,
) -> None:
    device_id = test_device_data[0]["id"]
    company_id = test_device_data[0]["company_id"]

    device_object = await device_repo.get_device_by_id(
        device_id=device_id,
        company_id=company_id,
    )
    assert device_object is not None

    await device_repo.delete_device(
        device_id=device_id,
        company_id=company_id,
    )
    device_object = await device_repo.get_device_by_id(
        device_id=device_id,
        company_id=company_id,
    )
    assert device_object is None
