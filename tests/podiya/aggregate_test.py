from podiya.aggregate import Aggregate


def test_agggregate():
    aggregate = Aggregate()
    assert aggregate._state is None
