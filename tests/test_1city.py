from modules import file_handle
from modules import openMapsImporter


def test_create_city_from_coordinates_small():
    """
    Tests for creating a city from coordinates small
    :return:
    """
    openMapsImporter.create_city("test_import_small", 21.00847, 52.22935, 21.01422, 52.23239, 1000, False)
    file_handle.load_city()


def test_create_city_from_coordinates_big():
    """
    Tests for creating a city from coordinates big (not yet implemented)
    :return:
    """
    # openMapsImporter.create_city("test_import_big", 21.00847, 52.22935, 21.01422, 52.23239, 1000, True)
    # file_handle.load_city()
    pass


def test_create_empty_city():
    """
    Tests for creating an empty city
    :return:
    """
    file_handle.create_empty_city("test_empty")
    file_handle.load_city()
