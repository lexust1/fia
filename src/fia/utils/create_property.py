"""The module helps to create a property.

The function simplifies the creation process of similar properties and
checks that the value of the property is a string.

Functions:
    - create_property: Simplifies the work with similar property
      getters and setters of the TvDataCollector class.
"""
import logging


# Set the module logger.
logger = logging.getLogger(__name__)


# Set properties for TvDataCollector.
def create_property(property_name: str) -> property:
    """Creates a property for TVDataCollector class.

    Takes a string name and creates a property with getter and setter
    for the TVDataCollector. The function simplifies the creation
    process of similar properties and checks that the value of
    the property is a string.

    Args:
        property_name: The name of a property ("exchange", "username",
            etc.)

    Returns:
        prop: A property for the class.
    """
    # TODO: correct str and property after the answer from GitHub
    # Add an underscore.
    protected_property_name = f"_{property_name}"

    @property  # type: ignore
    def prop(self) -> str:
        """The getter and setter.

        The getter gets the value of the property. The setter checks
        that the value is a string and sets the value for the current
        protected_property_name.

        Args:
            value: A string variable for a property used in the setter.

        Returns:
            protected_property_name: A property name with an additional
                single underscore _ in the beginning returned by the
                getter.

        Raises:
            SystemExit: If the setter see that the value is not
                a string and not empty string.
        """
        return getattr(self, protected_property_name)

    @prop.setter
    def prop(self, value: str) -> None:
        if isinstance(value, str) and value != "" and value != " ":
            setattr(self, protected_property_name, value)
        else:
            logger.error(f"The {property_name} value has to be not an empty "
                         f"string.",
                         exc_info=True,
                         stack_info=True)
            raise SystemExit(f"The {property_name} value has to be not an "
                             f"empty string.")
    return prop  # type: ignore
