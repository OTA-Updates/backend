import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.groups.models import Group
from calypte_api.groups.repositories import GroupRepo
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
