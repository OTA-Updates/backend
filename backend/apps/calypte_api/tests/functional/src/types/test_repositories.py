import random

from datetime import datetime
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from calypte_api.types.models import Type
from calypte_api.types.repository import TypeRepo
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def type_repo(db_session: AsyncSession):
    return TypeRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_type_data(db_session: AsyncSession):
    company_ids = [uuid4() for _ in range(10)]
    values = [
        {
            "id": uuid4(),
            "company_id": random.choice(company_ids),
            "name": f"test name {i}",
            "description": f"test description {i}",
            "created_at": datetime.now(),
        }
        for i in range(100)
    ]
    await db_session.execute(insert(Type).values(values))
    await db_session.commit()
    return values


async def test_get_type_by_id(test_type_data: list[dict], type_repo: TypeRepo) -> None:
    expected_type = test_type_data[0]
    type_object = await type_repo.get_type_by_id(
        company_id=expected_type["company_id"],
        type_id=expected_type["id"],
    )

    assert type_object.id == expected_type["id"]
    assert type_object.name == expected_type["name"]
    assert type_object.description == expected_type["description"]


@pytest.mark.parametrize(
    "limit, offset",
    [
        (1, 0),
        (5, 2),
        (20, 100),
    ],
)
async def test_get_types(
    test_type_data: list[dict], type_repo: TypeRepo, limit: int, offset: int
) -> None:
    command_id = test_type_data[0]["company_id"]
    type_object = await type_repo.get_types(
        company_id=command_id,
        name=None,
        limit=limit,
        offset=offset,
    )

    expected_types = [
        type_data
        for type_data in test_type_data
        if type_data["company_id"] == command_id
    ]

    expected_types = expected_types[offset : offset + limit]
    expected_types.sort(key=lambda x: x["created_at"])

    assert len(type_object) == len(expected_types)
    for type_object, expected_type in zip(type_object, expected_types):
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
