from uuid import UUID

from fastapi import HTTPException


class ObjectNotFoundError(HTTPException):
    def __init__(
        self, object_id: UUID, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(
            status_code=404,
            detail=f"object {object_id} not found",
            headers=headers,
        )


class DatabaseError(HTTPException):
    def __init__(
        self, detail: str, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status_code=400, detail=detail, headers=headers)


class RepositoryError(BaseException):
    ...
