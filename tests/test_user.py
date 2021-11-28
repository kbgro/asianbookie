import pytest

from asianbookie.domain import AsianBookieUser


def test_user_equality():
    user = AsianBookieUser.from_profile("kopikia", 12, "index.cfm?player=kopikia&ID=382731", 12_000_000, 6)
    user1 = AsianBookieUser.from_profile("Nonkopir", 12, "index.cfm?player=Nonkopir&ID=658433", 12_000_000, 6)
    user2 = None
    assert user == user
    assert hash(user) == hash(user)
    assert user != user1
    assert user != user2


def test_from_profile():
    user = AsianBookieUser.from_profile("kopikia", 12, "index.cfm?player=kopikia&ID=382731", 12_000_000, 6)
    assert isinstance(user, AsianBookieUser)
    assert user.balance == 12_000_000
    assert user.followers != 8
    assert user.user_id == 382731
    assert str(user) == "AsianBookieUser(name=kopikia, rank=12)"
    assert repr(user) == "< AsianBookieUser(name=kopikia, rank=12) >"


def test_from_kwargs():
    with pytest.raises(AttributeError):
        _ = AsianBookieUser.from_profile("kopikia", 12, "index.cfm?player=kopikia&ID=382731", 12_000_000, 6, age=25)
