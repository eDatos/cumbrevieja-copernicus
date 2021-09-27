from copernicus import storage


def test_operations():
    status = storage.set_value('test', 1, namespace='test-copernicus-cumprevieja')
    assert status is True
    value = storage.get_value('test', namespace='test-copernicus-cumprevieja', cast=int)
    assert value == 1
