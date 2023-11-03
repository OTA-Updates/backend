import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.common.models import device_tag_lookup
from calypte_api.devices.models import Device
from calypte_api.devices.repository import DeviceRepo
from calypte_api.firmware_info.models import FirmwareInfo
from calypte_api.tags.models import Tag
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

    tag_values = []
    for i in range(100):
        type_obj = random.choice(type_values)
        tag_values.append(
            {
                "id": uuid4(),
                "company_id": type_obj["company_id"],
                "type_id": type_obj["id"],
                "name": f"test name {i}",
                "color": "#000000",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(Tag).values(tag_values))

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

    device_values = []
    for i in range(100):
        type_obj = random.choice(type_values)
        firmware_obj = random.choice(firmware_values)
        device_values.append(
            {
                "id": uuid4(),
                "company_id": type_obj["company_id"],
                "type_id": type_obj["id"],
                "serial_number": f"serial number {i}",
                "current_firmware_id": firmware_obj["id"],
                "registered_at": random.choice([datetime.now(), None]),
                "name": f"test name {i}",
                "description": f"test description {i}",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(Device).values(device_values))

    device_tag_values = []
    for device in device_values:
        tags_ids = {tag["id"] for tag in random.choices(tag_values, k=4)}
        device["tags"] = list(tags_ids)
        for tag_id in tags_ids:
            device_tag_values.append(
                {
                    "device_id": device["id"],
                    "tag_id": tag_id,
                }
            )
    await db_session.execute(
        insert(device_tag_lookup).values(device_tag_values)
    )

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
    "limit, offset, name, serial_number, type_id_filter, tags_filter, firmware_info_filter",  # noqa
    [
        (5, 1, None, None, False, False, False),
        (5, 0, "test name 1", None, False, False, False),
        (5, 0, None, "serial number 1", False, False, False),
        (5, 0, "test name 1", None, False, False, False),
        (5, 0, None, None, True, False, False),
        (5, 0, None, None, False, True, False),
        (5, 0, None, None, False, False, True),
        (5, 0, "test name 1", "serial number", True, True, True),
    ],
)
async def test_get_devices(
    test_device_data: list[dict],
    device_repo: DeviceRepo,
    limit: int,
    offset: int,
    name: str | None,
    serial_number: str | None,
    type_id_filter: bool,
    tags_filter: bool,
    firmware_info_filter: bool,
) -> None:
    command_id = test_device_data[0]["company_id"]
    type_id = None
    tags = None
    current_firmware_id = None

    if type_id_filter:
        type_id = test_device_data[0]["type_id"]
    if tags_filter:
        tags = test_device_data[0]["tags"][:1]
    if firmware_info_filter:
        current_firmware_id = test_device_data[0]["current_firmware_id"]

    device_objects = await device_repo.get_devices(
        company_id=command_id,
        serial_number=serial_number,
        type_id=type_id,
        current_firmware_id=current_firmware_id,
        name=name,
        tags=tags,
        limit=limit,
        offset=offset,
    )

    expected_devices = [
        device_data
        for device_data in test_device_data
        if (device_data["company_id"] == command_id)
        and (name is None or device_data["name"] in name)
        and (
            serial_number is None
            or device_data["serial_number"] == serial_number
        )
        and (type_id is None or device_data["type_id"] == type_id)
        and (tags is None or set(tags).issubset(device_data["tags"]))
        and (
            current_firmware_id is None
            or device_data["current_firmware_id"] == current_firmware_id
        )
    ]

    expected_devices = expected_devices[offset : offset + limit]
    expected_devices.sort(key=lambda x: x["created_at"])

    assert len(device_objects) == len(expected_devices)

    for device_object, expected_device in zip(
        device_objects, expected_devices
    ):
        assert device_object.id == expected_device["id"]
        assert device_object.name == expected_device["name"]
        assert device_object.description == expected_device["description"]


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
        "tags": expected_device["tags"],
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
        "tags": expected_device["tags"],
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
