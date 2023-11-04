import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.firmware_info.models import FirmwareInfo
from calypte_api.groups.models import Group
from calypte_api.groups.repository import GroupRepo
from calypte_api.types.models import Type
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def groups_repo(db_session: AsyncSession):
    return GroupRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_groups_data(
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
        firmware = random.choice(firmware_values)
        group_values.append(
            {
                "id": uuid4(),
                "company_id": firmware["company_id"],
                "type_id": firmware["type_id"],
                "name": f"test name {i}",
                "assigned_firmware_id": firmware["id"],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    await db_session.execute(insert(Group).values(group_values))

    await db_session.commit()
    return group_values


async def test_get_groups_by_id(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
) -> None:
    exp_groups = test_groups_data[0]
    groups_object = await groups_repo.get_group_by_id(
        company_id=exp_groups["company_id"],
        group_id=exp_groups["id"],
    )
    assert groups_object is not None
    assert groups_object.id == exp_groups["id"]
    assert groups_object.name == exp_groups["name"]
    assert groups_object.company_id == exp_groups["company_id"]
    assert groups_object.type_id == exp_groups["type_id"]
    assert (
        groups_object.assigned_firmware_id
        == exp_groups["assigned_firmware_id"]
    )


@pytest.mark.parametrize(
    "limit, offset, name, type_id_filter",
    [
        (5, 1, None, False),
        (5, 0, None, False),
        (5, 1, "test group", False),
        (5, 1, None, True),
        (5, 1, None, False),
        (5, 1, "test group", True),
    ],
)
async def test_get_groups(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
    limit: int,
    offset: int,
    name: str | None,
    type_id_filter: bool,
) -> None:
    command_id = test_groups_data[0]["company_id"]
    type_id = None

    if type_id_filter:
        type_id = test_groups_data[0]["type_id"]

    groups_objects = await groups_repo.get_groups(
        company_id=command_id,
        type_id=type_id,
        name=name,
        limit=limit,
        offset=offset,
    )

    expected_groups = [
        groups_data
        for groups_data in test_groups_data
        if (groups_data["company_id"] == command_id)
        and (name is None or groups_data["name"] == name)
        and (type_id is None or groups_data["type_id"] == type_id)
    ]

    end = offset + limit
    expected_groups = expected_groups[offset:end]
    expected_groups.sort(key=lambda x: x["created_at"])

    assert len(groups_objects) == len(expected_groups)

    for groups_object, expected_group in zip(groups_objects, expected_groups):
        assert groups_object.id == expected_group["id"]
        assert groups_object.name == expected_group["name"]


@pytest.mark.parametrize(
    "groups",
    [
        {
            "name": "test name",
            "company_id": uuid4(),
        }
    ],
)
async def test_create_groups(
    groups_repo: GroupRepo,
    test_groups_data: list[dict],
    groups: dict,
) -> None:
    expected_groups = test_groups_data[0]

    new_groups = {
        **groups,
        "type_id": expected_groups["type_id"],
        "assigned_firmware_id": expected_groups["assigned_firmware_id"],
    }

    groups_object = await groups_repo.create_group(**new_groups)
    assert groups_object.name == groups["name"]
    assert groups_object.company_id == groups["company_id"]


@pytest.mark.parametrize(
    "groups",
    [
        {
            "name": "test name",
        }
    ],
)
async def test_update_groups(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
    groups: dict,
) -> None:
    expected_groups = test_groups_data[0]

    new_groups = {
        **groups,
        "company_id": expected_groups["company_id"],  # type: ignore
        "group_id": expected_groups["id"],
        "assigned_firmware_id": expected_groups["assigned_firmware_id"],
    }

    groups_object = await groups_repo.update_group(**new_groups)

    assert groups_object.name == new_groups["name"]
    assert groups_object.id == new_groups["group_id"]


async def test_delete_group(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
) -> None:
    group_id = test_groups_data[0]["id"]
    company_id = test_groups_data[0]["company_id"]

    group_object = await groups_repo.get_group_by_id(
        group_id=group_id,
        company_id=company_id,
    )
    assert group_object is not None

    await groups_repo.delete_group(
        group_id=group_id,
        company_id=company_id,
    )
    group_object = await groups_repo.get_group_by_id(
        group_id=group_id,
        company_id=company_id,
    )
    assert group_object is None


async def test_check_groups_belongs_to(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
) -> None:
    expected_groups = test_groups_data[0]

    assert await groups_repo.check_groups_belongs_to(
        group_id=expected_groups["id"],
        company_id=expected_groups["company_id"],
    )


async def test_check_groups_does_not_belong_to(
    test_groups_data: list[dict],
    groups_repo: GroupRepo,
) -> None:
    expected_groups = test_groups_data[0]

    assert not await groups_repo.check_groups_belongs_to(
        group_id=expected_groups["id"],
        company_id=uuid4(),
    )
