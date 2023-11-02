import random

from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from calypte_api.tags.models import Tag
from calypte_api.tags.repository import TagRepo
from calypte_api.types.models import Type
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture(scope="function")
async def tags_repo(db_session: AsyncSession):
    return TagRepo(db_session=db_session)


@pytest_asyncio.fixture(scope="function")
async def test_tags_data(
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

    await db_session.commit()
    return tag_values


async def test_get_tags_by_id(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
) -> None:
    exp_tags = test_tags_data[0]
    tags_object = await tags_repo.get_tag_by_id(
        company_id=exp_tags["company_id"],
        tag_id=exp_tags["id"],
    )
    assert tags_object.id == exp_tags["id"]
    assert tags_object.name == exp_tags["name"]
    assert tags_object.company_id == exp_tags["company_id"]
    assert tags_object.type_id == exp_tags["type_id"]


@pytest.mark.parametrize(
    "limit, offset, name, type_id_filter",
    [
        (5, 1, None, False),
        (5, 0, None, False),
        (5, 1, "test tag", False),
        (5, 1, None, True),
        (5, 1, None, False),
        (5, 1, "test tag", True),
    ],
)
async def test_get_tags(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
    limit: int,
    offset: int,
    name: str | None,
    type_id_filter: bool,
) -> None:
    command_id = test_tags_data[0]["company_id"]
    type_id = None

    if type_id_filter:
        type_id = test_tags_data[0]["type_id"]

    tags_objects = await tags_repo.get_tags(
        company_id=command_id,
        type_id=type_id,
        name=name,
        limit=limit,
        offset=offset,
    )

    expected_tags = [
        tags_data
        for tags_data in test_tags_data
        if (tags_data["company_id"] == command_id)
        and (name is None or tags_data["name"] == name)
        and (type_id is None or tags_data["type_id"] == type_id)
    ]

    expected_tags = expected_tags[offset : offset + limit]
    expected_tags.sort(key=lambda x: x["created_at"])

    assert len(tags_objects) == len(expected_tags)

    for tags_object, expected_tags in zip(tags_objects, expected_tags):
        assert tags_object.id == expected_tags["id"]
        assert tags_object.name == expected_tags["name"]


@pytest.mark.parametrize(
    "tags",
    [
        {
            "name": "test name",
            "color": "#000000",
            "company_id": uuid4(),
        }
    ],
)
async def test_create_tags(
    tags_repo: TagRepo,
    test_tags_data: list[dict],
    tags: dict,
) -> None:
    expected_tags = test_tags_data[0]

    new_tags = {
        **tags,
        "type_id": expected_tags["type_id"],
    }

    tags_object = await tags_repo.create_tag(**new_tags)
    assert tags_object.name == tags["name"]
    assert tags_object.company_id == tags["company_id"]


@pytest.mark.parametrize(
    "tags",
    [
        {
            "name": "test name",
            "color": "#000000",
        }
    ],
)
async def test_update_tags(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
    tags: dict,
) -> None:
    expected_tags = test_tags_data[0]

    new_tags = {
        **tags,
        "company_id": expected_tags["company_id"],  # type: ignore
        "tag_id": expected_tags["id"],
    }

    tags_object = await tags_repo.update_tag(**new_tags)

    assert tags_object.name == new_tags["name"]
    assert tags_object.id == new_tags["tag_id"]


async def test_delete_tag(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
) -> None:
    tag_id = test_tags_data[0]["id"]
    company_id = test_tags_data[0]["company_id"]

    tag_object = await tags_repo.get_tag_by_id(
        tag_id=tag_id,
        company_id=company_id,
    )
    assert tag_object is not None

    await tags_repo.delete_tag(
        tag_id=tag_id,
        company_id=company_id,
    )
    tag_object = await tags_repo.get_tag_by_id(
        tag_id=tag_id,
        company_id=company_id,
    )
    assert tag_object is None


async def test_check_tags_belongs_to(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
) -> None:
    expected_tags = test_tags_data[0]

    assert await tags_repo.check_tags_belongs_to(
        tags=[expected_tags["id"]],
        company_id=expected_tags["company_id"],
    )


async def test_check_tags_does_not_belong_to(
    test_tags_data: list[dict],
    tags_repo: TagRepo,
) -> None:
    expected_tags = test_tags_data[0]

    assert not await tags_repo.check_tags_belongs_to(
        tags=[expected_tags["id"]],
        company_id=uuid4(),
    )
