from typing import Dict

import pytest

from asianbookie import top100_users, upcoming_matches
from asianbookie.domain import AsianBookieUser


@pytest.fixture
def matches():
    return upcoming_matches()


@pytest.fixture
def top100users() -> Dict[int, AsianBookieUser]:
    return {user.rank: user for user in top100_users()}
