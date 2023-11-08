import random

from datetime import datetime
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from calypte_api.types.models import Type
from calypte_api.types.repositories import TypeRepo
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def type_repo(db_session: AsyncSession):
    return TypeRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_type_data(db_session: AsyncSession):
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
    await db_session.commit()
    return type_values


async def test_get_type_by_id(
    test_type_data: list[dict],
    type_repo: TypeRepo,
) -> None:
    expected_type = test_type_data[0]
    type_object = await type_repo.get_type_by_id(
        company_id=expected_type["company_id"],
        type_id=expected_type["id"],
    )

    assert type_object.id == expected_type["id"]
    assert type_object.name == expected_type["name"]
    assert type_object.description == expected_type["description"]


@pytest.mark.parametrize(
    "company_id, name, description",
    [
        (
            uuid4(),
            "test name",
            "test description",
        ),
    ],
)
async def test_create_type(
    type_repo: TypeRepo,
    company_id: UUID,
    name: str,
    description: str | None,
) -> None:
    type_object = await type_repo.create_type(
        company_id=company_id,
        name=name,
        description=description,
    )
    assert type_object.name == name
    assert type_object.description == description
    assert type_object.company_id == company_id


@pytest.mark.parametrize(
    "name, description",
    [
        (
            "test name",
            "test description",
        ),
    ],
)
async def test_update_type(
    test_type_data: list[dict],
    type_repo: TypeRepo,
    name: str,
    description: str | None,
) -> None:
    type_id = test_type_data[0]["id"]
    company_id = test_type_data[0]["company_id"]
    type_object = await type_repo.update_type(
        type_id=type_id,
        company_id=company_id,
        name=name,
        description=description,
    )
    assert type_object.id == type_id
    assert type_object.name == name
    assert type_object.description == description


@pytest.mark.parametrize(
    "name, description",
    [
        (
            "test name",
            "test description",
        ),
    ],
)
async def test_delete_type(
    test_type_data: list[dict],
    type_repo: TypeRepo,
    name: str,
    description: str | None,
) -> None:
    type_id = test_type_data[0]["id"]
    company_id = test_type_data[0]["company_id"]

    type_object = await type_repo.get_type_by_id(
        type_id=type_id,
        company_id=company_id,
    )
    assert type_object is not None

    await type_repo.delete_type(
        type_id=type_id,
        company_id=company_id,
    )
    type_object = await type_repo.get_type_by_id(
        type_id=type_id,
        company_id=company_id,
    )
    assert type_object is None


async def test_check_type_does_belong_to_company(
    test_type_data: list[dict],
    type_repo: TypeRepo,
) -> None:
    type_id = test_type_data[0]["id"]
    company_id = test_type_data[0]["company_id"]

    type_object = await type_repo.check_type_belongs_to_company(
        type_id=type_id,
        company_id=company_id,
    )

    assert type_object is True


async def test_check_type_does_not_belong_to_company(
    test_type_data: list[dict],
    type_repo: TypeRepo,
) -> None:
    type_id = uuid4()
    company_id = test_type_data[0]["company_id"]

    type_object = await type_repo.check_type_belongs_to_company(
        type_id=type_id,
        company_id=company_id,
    )

    assert type_object is False
