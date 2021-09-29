from copernicus import cstorage


def test_operations():
    value = cstorage.set_value('test-copernicus', 1)
    assert value == '1'
    value = cstorage.get_value('test-copernicus', cast=int)
    assert value == 1
