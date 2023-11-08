import http

from collections.abc import Callable, Coroutine
from typing import Annotated

from calypte_api.common.authorization import JWTBearer, JwtClaims
from calypte_api.common.databases import (
    get_db_session,
    get_minio_client,
    get_redis_client,
)
from calypte_api.common.settings import get_settings

from fastapi import Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from fastapi_pagination import Params
from miniopy_async import Minio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


settings = get_settings()

DBSessionType = Annotated[AsyncSession, Depends(get_db_session)]
S3ClientType = Annotated[Minio, Depends(get_minio_client)]
RedisClientType = Annotated[Redis, Depends(get_redis_client)]
PaginationParamsType = Annotated[Params, Depends()]
UserTokenType = Annotated[JwtClaims, Depends(JWTBearer())]
RateLimiterType = Annotated[
    RateLimiter,
    Depends(
        RateLimiter(
            times=settings.rate_limiter_times,
            seconds=settings.rate_limiter_seconds,
        )
    ),
]

CheckPermissionType = Callable[
    [UserTokenType],
    Coroutine[None, None, JwtClaims],
]


def check_permission(user_role: str) -> CheckPermissionType:
    async def _check_permission(user_token: UserTokenType) -> JwtClaims:
        if user_role != user_token.user.role:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail=(
                    "User does not have a permission"
                    " to perform this action."
                ),
            )

        return user_token

    return _check_permission
