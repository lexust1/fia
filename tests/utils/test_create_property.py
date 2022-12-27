import pytest

from fia.utils.create_property import create_property


def test_type_return():
    """Tests the type of the returned data."""
    prop = create_property("username")
    assert isinstance(prop, property)


@pytest.fixture(scope="module")
def create_test_class():
    """Creates class the test class TestProperty."""
    class TestProperty:
        def __init__(self, username: str) -> None:
            self.username = username
        username = create_property("username")
    return TestProperty


def test_create_class_property(create_test_class):
    """Tests the class property creation."""
    assert isinstance(create_test_class.username, property)


def test_set_instance_property_name(create_test_class):
    """Tests the instance property name."""
    test_property = create_test_class("LogIN")
    assert (hasattr(test_property, "username") and
            hasattr(test_property, "_username"))


def test_set_instance_property_value_as_str(create_test_class):
    """Tests the instance setter of property value."""
    test_property = create_test_class("LogIN")
    assert getattr(test_property, "username") == "LogIN"


def test_get_instance_property_value(create_test_class):
    """Tests the instance getter of property value."""
    test_property = create_test_class("LogIN")
    assert test_property.username == "LogIN"


@pytest.mark.parametrize(
    "prop_value",
    [
        123,
        0,
        0.123,
        [],
        None,
        "",
        " "
    ]
)
def test_set_instance_property_value_not_string(prop_value, create_test_class):
    """Tests the raise when a property value is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        create_test_class(prop_value)
    expected = "The username value has to be not an empty string."
    assert exc_info.value.args[0] == expected


def test_missing_argument(create_test_class):
    """Tests the missing arguments."""
    with pytest.raises(TypeError) as exc_info:
        create_test_class()
    assert "missing 1 required positional argument" in exc_info.value.args[0]
