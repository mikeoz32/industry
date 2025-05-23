from datetime import datetime
from industry.accounts.entity.user import UserId
from industry.accounts.events.user import UserDisabledEvent, UserRegisteredEvent
from industry.accounts.mutators.user import UserMutator


user_mutator = UserMutator()

identity_id = "test_id"


def test_user_registered_mutation():
    event = UserRegisteredEvent(
        user_id=UserId.from_identity(identity_id),
        identity_id=identity_id,
        email="test_email",
        nickname="test_nickname",
        created_at=datetime.now(),
    )
    state = user_mutator(event, None)
    assert state
    event2 = UserDisabledEvent(user_id=state.user_id)
    state = user_mutator(event2, state)
    assert state.disabled is True
