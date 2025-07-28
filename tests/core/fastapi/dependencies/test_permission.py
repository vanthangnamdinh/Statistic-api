from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request

from app.container import Container
from core.fastapi.dependencies import (
    AllowAll,
    IsAuthenticated,
    PermissionDependency,
)
from core.fastapi.dependencies.permission import UnauthorizedException

container = Container()


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    # Given
    dependency = PermissionDependency(permissions=[IsAuthenticated])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    # When, Then
    with pytest.raises(UnauthorizedException):
        await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_allow_all():
    # Given
    dependency = PermissionDependency(permissions=[AllowAll])
    request = AsyncMock(spec=Request)

    # When
    sut = await dependency(request=request)

    # Then
    assert sut is None
