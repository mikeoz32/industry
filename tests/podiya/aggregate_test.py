from podiya.aggregate import Aggregate


def test_agggregate():
    aggregate = Aggregate()
    aggregate.apply({})
    assert aggregate._state is None
